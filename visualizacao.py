import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def construir_subgrafo_nx(adj, centro=None, caminho=None, limite_vizinhos=12):
    """
    Constrói um objeto NetworkX com poucos vizinhos para manter a clareza.
    """
    G = nx.Graph()
    nos_interesse = set()
    
    if caminho:
        nos_interesse.update(caminho)
        for no in caminho:
            # Reduzindo para pegar apenas os vizinhos mais relevantes
            vizinhos = sorted(adj[no].items(), key=lambda x: x[1], reverse=True)[:limite_vizinhos]
            for v, peso in vizinhos:
                nos_interesse.add(v)
    elif centro:
        nos_interesse.add(centro)
        vizinhos = sorted(adj[centro].items(), key=lambda x: x[1], reverse=True)[:limite_vizinhos]
        for v, peso in vizinhos:
            nos_interesse.add(v)
    else:
        nos_ordenados = sorted(adj.keys(), key=lambda k: sum(adj[k].values()), reverse=True)[:20]
        nos_interesse.update(nos_ordenados)

    # Construir arestas com filtro de peso mais rigoroso
    for u in nos_interesse:
        if u not in adj: continue
        for v, peso in adj[u].items():
            if v in nos_interesse:
                e_do_caminho = caminho and (u in caminho and v in caminho)
                # Aumentei o filtro de peso para 2 para remover conexoes fracas
                if e_do_caminho or peso > 2: 
                    custo = 1.0 / peso if peso > 0 else float('inf')
                    G.add_edge(u, v, weight=peso, cost=custo)
                
    return G

def desenhar_grafo(G, caminho=None, titulo="Visualização de Rede"):
    """
    Renderiza o grafo com foco em clareza extrema.
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    fig.canvas.manager.set_window_title("Sistema de Analise de Grafos")
    
    # Titulo com indicacao de simplificacao
    titulo_completo = f"{titulo}\n(Visualizacao Simplificada)"
    plt.suptitle(titulo_completo, fontsize=18, fontweight='bold', color='#2c3e50', y=0.95)
    ax.axis('off')

    # Layout: k ainda maior (1.5) para separar bem os nos
    pos = nx.spring_layout(G, weight='weight', k=1.5, iterations=200, seed=42)

    # Cores e tamanhos
    node_colors = []
    node_sizes = []
    
    for node in G.nodes():
        grau = G.degree(node, weight='weight')
        # Tamanho dinâmico com base logarítmica para evitar nós gigantescos
        import math
        size_factor = math.log(grau + 1) * 300
        node_sizes.append(400 + size_factor)
        
        if caminho and node in caminho:
            if node == caminho[0]:
                node_colors.append('#27ae60') # Verde forte
            elif node == caminho[-1]:
                node_colors.append('#c0392b') # Vermelho forte
            else:
                node_colors.append('#f39c12') # Laranja (Caminho)
        else:
            node_colors.append('#3498db') # Azul suave

    # --- Renderização das Arestas ---
    
    # Arestas de Contexto (Finíssimas e transparentes)
    arestas_normais = [(u, v) for (u, v) in G.edges() if not (caminho and u in caminho and v in caminho)]
    if arestas_normais:
        nx.draw_networkx_edges(
            G, pos, edgelist=arestas_normais, 
            width=0.8, alpha=0.15, edge_color='#bdc3c7', ax=ax
        )

    # Arestas do Caminho (Destaque total)
    if caminho:
        arestas_caminho = []
        for i in range(len(caminho)-1):
            if G.has_edge(caminho[i], caminho[i+1]):
                arestas_caminho.append((caminho[i], caminho[i+1]))
        
        if arestas_caminho:
            # Efeito de brilho/glow na aresta (desenhando uma mais grossa por baixo)
            nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, width=6.0, alpha=0.3, edge_color='#f39c12', ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, width=2.5, alpha=1.0, edge_color='#d35400', ax=ax)

    # --- Renderização dos Nós ---
    nodes_collection = nx.draw_networkx_nodes(
        G, pos, 
        node_color=node_colors, 
        node_size=node_sizes, 
        alpha=0.95, 
        edgecolors='white', 
        linewidths=1.2, 
        ax=ax
    )

    # --- Rótulos com "Halo" para legibilidade ---
    labels = {n: n for n in G.nodes()}
    texts = nx.draw_networkx_labels(
        G, pos, labels=labels, 
        font_size=9, font_color='#2c3e50', font_weight='bold', 
        font_family='sans-serif', ax=ax
    )
    
    # Adicionando efeito de contorno (path effects) nos textos para ler sobre as linhas
    from matplotlib import patheffects
    for _, t in texts.items():
        t.set_path_effects([patheffects.withStroke(linewidth=3, foreground='white', alpha=0.8)])

    # --- Interatividade ---
    annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#bdc3c7", lw=1, alpha=0.9),
                        arrowprops=dict(arrowstyle="->", color="#34495e"),
                        fontsize=10)
    annot.set_visible(False)

    def update_annot(ind):
        idx = ind["ind"][0]
        node = list(G.nodes)[idx]
        xy = pos[node]
        annot.xy = xy
        
        vizinhos = len(list(G.neighbors(node)))
        peso_total = sum([G[node][v]['weight'] for v in G.neighbors(node)])
        
        texto = f"{node}\n"
        texto += f"Conexões: {vizinhos}\n"
        texto += f"Afinidade Total: {int(peso_total)}"
        
        if caminho and node in caminho:
            passo = caminho.index(node)
            texto += f"\nEtapa no Caminho: {passo + 1}"
            
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

    fig.canvas.mpl_connect("motion_notify_event", hover)
    
    # Legenda compacta
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Jogo Comum', markerfacecolor='#3498db', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Origem/Destino', markerfacecolor='#c0392b', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Caminho', markerfacecolor='#f39c12', markersize=8),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9, frameon=True, facecolor='white')

    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    plt.show()

def renderizar_interface(adj, jogo_origem=None, jogo_destino=None, caminho_otimo=None):
    """
    Ponto de entrada do módulo.
    """
    print("\n" + "-"*50)
    print(" INTERFACE GRAFICA ".center(50, '-'))
    print("-"*50)
    
    try:
        import networkx
    except ImportError:
        print("Erro: NetworkX nao instalado.")
        return
        
    try:
        import matplotlib
    except ImportError:
        print("Erro: Matplotlib nao instalado.")
        return

    if caminho_otimo and len(caminho_otimo) > 0:
        print(f"Status: Gerando visao do caminho otimo.")
        G = construir_subgrafo_nx(adj, caminho=caminho_otimo)
        titulo = f"Analise de Caminho: {jogo_origem} -> {jogo_destino}"
    elif jogo_origem:
        print(f"Status: Gerando vizinhanca de '{jogo_origem}'.")
        G = construir_subgrafo_nx(adj, centro=jogo_origem)
        titulo = f"Ecossistema: {jogo_origem}"
    else:
        print("Status: Gerando mapa global.")
        G = construir_subgrafo_nx(adj)
        titulo = "Visao Global de Conexoes"
        
    print(f"Grafo: {G.number_of_nodes()} nos, {G.number_of_edges()} arestas.")
    print("Dica: Use o mouse para interagir e ver detalhes.")
    
    desenhar_grafo(G, caminho=caminho_otimo, titulo=titulo)
