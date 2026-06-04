import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def construir_subgrafo_nx(adj, centro=None, caminho=None, limite_vizinhos=15):
    """
    Constrói um objeto NetworkX a partir do dicionário de adjacências.
    Para evitar uma rede ilegível com milhares de nós, filtra o grafo 
    baseando-se em um caminho específico ou em um nó central.
    """
    G = nx.Graph()
    
    nos_interesse = set()
    
    if caminho:
        nos_interesse.update(caminho)
        # Adicionar vizinhos do caminho para dar contexto à rede
        for no in caminho:
            # Ordena vizinhos pela força da conexão (peso)
            vizinhos = sorted(adj[no].items(), key=lambda x: x[1], reverse=True)[:limite_vizinhos]
            for v, peso in vizinhos:
                nos_interesse.add(v)
    elif centro:
        nos_interesse.add(centro)
        # Traz um raio de vizinhos ao redor do centro
        vizinhos = sorted(adj[centro].items(), key=lambda x: x[1], reverse=True)[:limite_vizinhos * 2]
        for v, peso in vizinhos:
            nos_interesse.add(v)
    else:
        # Visão geral: Pega os nós com maior número de conexões globais
        nos_ordenados = sorted(adj.keys(), key=lambda k: sum(adj[k].values()), reverse=True)[:limite_vizinhos * 3]
        nos_interesse.update(nos_ordenados)

    # Construir o grafo do NetworkX com as arestas relevantes
    for u in nos_interesse:
        if u not in adj: continue
        for v, peso in adj[u].items():
            if v in nos_interesse:
                # O custo no dijkstra original é 1.0 / peso.
                custo = 1.0 / peso if peso > 0 else float('inf')
                G.add_edge(u, v, weight=peso, cost=custo)
                
    return G

def desenhar_grafo(G, caminho=None, titulo="Visualização de Rede"):
    """
    Renderiza o grafo utilizando NetworkX e Matplotlib com interatividade
    (hover, zoom e pan).
    """
    # Configuração de design profissional
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.canvas.manager.set_window_title("Sistema de Análise de Grafos")
    ax.set_title(titulo, fontsize=16, fontweight='bold', color='#333333', pad=20)
    ax.axis('off')

    # Utilizando um layout de mola iterativo com base nos pesos para organizar os nós
    pos = nx.spring_layout(G, weight='weight', k=0.7, iterations=100, seed=42)

    # Preparação de cores e tamanhos seguindo uma hierarquia visual
    node_colors = []
    node_sizes = []
    
    for node in G.nodes():
        grau = G.degree(node, weight='weight')
        # Tamanho dinâmico baseado na importância do nó na rede
        node_sizes.append(300 + grau * 10)
        
        if caminho and node in caminho:
            if node == caminho[0]:
                node_colors.append('#2ecc71') # Origem: Verde Esmeralda
            elif node == caminho[-1]:
                node_colors.append('#e74c3c') # Destino: Vermelho Alizarin
            else:
                node_colors.append('#f1c40f') # Caminho Intermediário: Amarelo Girassol
        else:
            node_colors.append('#3498db') # Padrão: Azul Peter River

    # Normalizar tamanhos dos nós para não cobrirem a tela
    max_size = max(node_sizes) if node_sizes else 1
    node_sizes = [min(s / max_size * 2500, 2500) for s in node_sizes]
    node_sizes = [max(s, 400) for s in node_sizes]

    # --- Renderização das Arestas ---
    
    # Arestas normais (contexto)
    arestas_normais = [(u, v) for (u, v) in G.edges() if not (caminho and u in caminho and v in caminho)]
    if arestas_normais:
        pesos_normais = [G[u][v]['weight'] for u, v in arestas_normais]
        max_peso = max(pesos_normais) if pesos_normais else 1
        larguras_normais = [0.5 + (w / max_peso) * 1.5 for w in pesos_normais]
        nx.draw_networkx_edges(G, pos, edgelist=arestas_normais, width=larguras_normais, alpha=0.3, edge_color='#bdc3c7', ax=ax)

    # Arestas em destaque (solução do Dijkstra)
    if caminho:
        arestas_caminho = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1) if G.has_edge(caminho[i], caminho[i+1])]
        if arestas_caminho:
            # Pegando os custos para exibir interatividade posteriormente
            nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, width=3.0, alpha=0.9, edge_color='#e67e22', ax=ax)

    # --- Renderização dos Nós e Rótulos ---
    nodes_collection = nx.draw_networkx_nodes(
        G, pos, 
        node_color=node_colors, 
        node_size=node_sizes, 
        alpha=0.9, 
        edgecolors='white', 
        linewidths=1.5, 
        ax=ax
    )

    # Limitar o tamanho do rótulo para manter a interface limpa
    labels = {n: (n[:15]+'...' if len(n)>18 else n) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='#2c3e50', font_weight='bold', font_family='sans-serif', ax=ax)

    # --- Interatividade: Informações ao Hover ---
    annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round4,pad=0.8", fc="#ffffff", ec="#bdc3c7", lw=1, alpha=0.95),
                        arrowprops=dict(arrowstyle="->", color="#34495e", lw=1.5),
                        fontsize=9, color="#2c3e50")
    annot.set_visible(False)

    def update_annot(ind):
        idx = ind["ind"][0]
        node = list(G.nodes)[idx]
        xy = pos[node]
        annot.xy = xy
        
        # Coletar métricas do nó
        vizinhos = len(list(G.neighbors(node)))
        peso_total = sum([G[node][v]['weight'] for v in G.neighbors(node)])
        
        texto = f"Jogo: {node}\n"
        texto += f"Vizinhos: {vizinhos}\n"
        texto += f"Força Total (Interseção): {peso_total}"
        
        if caminho and node in caminho:
            passo = caminho.index(node)
            texto += f"\nEtapa no Caminho: {passo}"
            
        annot.set_text(texto)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = nodes_collection.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    # Conectar o evento de mouse ao figure do matplotlib
    fig.canvas.mpl_connect("motion_notify_event", hover)
    
    # --- Legenda Profissional ---
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Jogo Relacionado', markerfacecolor='#3498db', markersize=10),
        Line2D([0], [0], color='#bdc3c7', lw=2, label='Conexão de Afinidade', alpha=0.5)
    ]
    if caminho:
        legend_elements.extend([
            Line2D([0], [0], marker='o', color='w', label='Origem', markerfacecolor='#2ecc71', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Destino', markerfacecolor='#e74c3c', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Caminho Ótimo', markerfacecolor='#f1c40f', markersize=10),
            Line2D([0], [0], color='#e67e22', lw=3, label='Arco de Transição')
        ])
    
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, shadow=False, fancybox=True, edgecolor='#bdc3c7')

    plt.tight_layout()
    plt.show()

def renderizar_interface(adj, jogo_origem=None, jogo_destino=None, caminho_otimo=None):
    """
    Ponto de entrada do módulo. Responsável por avaliar os dados disponíveis,
    construir a estrutura NetworkX e iniciar a interface gráfica.
    """
    print("\n" + "="*50)
    print("🖥️  INICIANDO INTERFACE GRÁFICA".center(50))
    print("="*50)
    
    try:
        import networkx
    except ImportError:
        print("[Erro] Biblioteca NetworkX não encontrada. Instale com: pip install networkx")
        return
        
    try:
        import matplotlib
    except ImportError:
        print("[Erro] Biblioteca Matplotlib não encontrada. Instale com: pip install matplotlib")
        return

    if caminho_otimo and len(caminho_otimo) > 0:
        print(f"[*] Gerando visualização focada no caminho ótimo.")
        G = construir_subgrafo_nx(adj, caminho=caminho_otimo)
        titulo = f"Análise de Caminho: {jogo_origem} -> {jogo_destino}"
    elif jogo_origem:
        print(f"[*] Gerando visualização da vizinhança de '{jogo_origem}'.")
        G = construir_subgrafo_nx(adj, centro=jogo_origem)
        titulo = f"Ecossistema: {jogo_origem}"
    else:
        print("[*] Nenhuma origem definida. Gerando mapa global do topo da rede.")
        G = construir_subgrafo_nx(adj)
        titulo = "Visão Global dos Jogos Mais Conectados"
        
    print(f"[*] Grafo processado: {G.number_of_nodes()} nós ativos e {G.number_of_edges()} arestas.")
    print("\n[!] DICAS DE INTERAÇÃO:")
    print("  - Utilize a barra inferior para dar Zoom e Pan na visualização.")
    print("  - Passe o mouse sobre os círculos (nós) para ver estatísticas detalhadas.")
    print("  - O grafo é gerado dinamicamente para priorizar a leitura.")
    
    desenhar_grafo(G, caminho=caminho_otimo, titulo=titulo)
