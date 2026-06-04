import networkx as nx
from collections import defaultdict
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# ── ETAPA 1: BASE DE CONHECIMENTO (TAXONOMIA ÂNCORA) ──────────────────────
# Como o dataset original não possui a coluna de "Gênero", ancoramos manualmente
# os jogos mais populares da Steam (que concentram >80% das conexões).
# Esses jogos servirão de "Sementes" para o algoritmo infectar o resto do grafo.
ANCORAS_GENERO = {
    # FPS & Shooters
    "Counter-Strike Global Offensive": "FPS Tático",
    "Counter-Strike": "FPS Tático",
    "Counter-Strike Source": "FPS Tático",
    "Team Fortress 2": "Hero Shooter",
    "Left 4 Dead 2": "Co-op Shooter",
    "Borderlands 2": "Looter Shooter",
    "Borderlands": "Looter Shooter",
    "PAYDAY 2": "Co-op Shooter",
    "Warframe": "Looter Shooter",
    "Call of Duty Modern Warfare 2": "FPS Ação",
    "Call of Duty Black Ops II": "FPS Ação",
    
    # RPG & Imersão
    "The Elder Scrolls V Skyrim": "RPG Mundo Aberto",
    "Fallout New Vegas": "RPG Mundo Aberto",
    "Fallout 4": "RPG Mundo Aberto",
    "The Witcher 3 Wild Hunt": "RPG Mundo Aberto",
    "Mount & Blade Warband": "RPG Sandbox",
    "Dark Souls": "Action RPG",
    
    # MOBA
    "Dota 2": "MOBA",
    "Smite": "MOBA",
    
    # Estratégia / RTS / 4X
    "Sid Meier's Civilization V": "Estratégia 4X",
    "XCOM Enemy Unknown": "Estratégia Tática",
    "Age of Empires II HD Edition": "RTS",
    "Total War ROME II - Emperor Edition": "Estratégia Grandiosa",
    "Total War SHOGUN 2": "Estratégia Grandiosa",
    "Company of Heroes 2": "RTS",
    "Europa Universalis IV": "Estratégia Grandiosa",
    "Stellaris": "Estratégia 4X",
    
    # Sobrevivência / Sandbox / Construção
    "Garry's Mod": "Sandbox Sandbox",
    "Rust": "Survival Multiplayer",
    "ARK Survival Evolved": "Survival Multiplayer",
    "DayZ": "Survival Multiplayer",
    "Unturned": "Survival Multiplayer",
    "Terraria": "Sandbox Survival",
    "Don't Starve Together": "Survival Co-op",
    "Space Engineers": "Sandbox Construção",
    
    # Simulação & Esporte
    "Football Manager 2015": "Simulação Esportiva",
    "Football Manager 2014": "Simulação Esportiva",
    "Football Manager 2013": "Simulação Esportiva",
    "Euro Truck Simulator 2": "Simulação Veicular",
    "Rocket League": "Esporte Ação",
    "Kerbal Space Program": "Simulação Espacial",
    
    # Mundo Aberto / Ação
    "Grand Theft Auto V": "Mundo Aberto Ação",
    "Grand Theft Auto IV": "Mundo Aberto Ação",
    "Tomb Raider": "Mundo Aberto Ação",
    
    # Indie / Roguelike
    "The Binding of Isaac Rebirth": "Roguelike",
    "FTL Faster Than Light": "Roguelike Estratégico",
    "Rogue Legacy": "Roguelike"
}

def agrupar_macro_generos(genero_detalhado):
    """
    Agrupa os subgêneros da taxonomia em Macro-Gêneros para facilitar
    a identificação do perfil principal do jogador.
    """
    g = genero_detalhado.lower()
    if "fps" in g or "shooter" in g: return "Shooter/FPS"
    if "rpg" in g: return "RPG"
    if "moba" in g: return "MOBA"
    if "estratégia" in g or "rts" in g or "4x" in g: return "Estratégia"
    if "survival" in g or "sandbox" in g: return "Survival/Sandbox"
    if "simulação" in g or "esporte" in g: return "Esportes/Simulação"
    if "mundo aberto" in g: return "Mundo Aberto"
    if "roguelike" in g or "indie" in g: return "Roguelike/Indie"
    return "Outros"

# ── ETAPA 2: PROPAGAÇÃO DE GÊNEROS (LABEL PROPAGATION) ────────────────────
def calcular_jaccard_e_propagar_generos(usuarios, adj):
    """
    1. Calcula o total de jogadores únicos por jogo.
    2. Usa isso para calcular a Similaridade de Jaccard (interseção / união).
    3. Usa Label Propagation para inferir o gênero dos jogos desconhecidos
       com base nos seus vizinhos mais similares.
    """
    # 1. Total de jogadores únicos por jogo
    total_jogadores = defaultdict(int)
    for user, jogos_dict in usuarios.items():
        for jogo in jogos_dict.keys():
            total_jogadores[jogo] += 1
            
    # 2. Inicializar o mapeamento de gêneros
    mapa_generos = {}
    macro_generos = {}
    
    # Sementes (Âncoras)
    for jogo, genero in ANCORAS_GENERO.items():
        if jogo in total_jogadores:
            mapa_generos[jogo] = genero
            macro_generos[jogo] = agrupar_macro_generos(genero)

    # 3. Label Propagation em Grafo Baseado em Jaccard
    # Vamos iterar 3 vezes para garantir que a infecção propague profundamente
    jogos_nao_classificados = [j for j in total_jogadores.keys() if j not in mapa_generos]
    
    for iteracao in range(3):
        novos_generos = {}
        
        for jogo in jogos_nao_classificados:
            pontuacao_genero = defaultdict(float)
            
            # Avaliar vizinhos
            for vizinho, intersecao in adj[jogo].items():
                if vizinho in mapa_generos:
                    # Similaridade de Jaccard: |A ∩ B| / (|A| + |B| - |A ∩ B|)
                    uniao = total_jogadores[jogo] + total_jogadores[vizinho] - intersecao
                    if uniao > 0:
                        jaccard = intersecao / uniao
                        
                        # O peso do vizinho é a similaridade multiplicada pela força da interseção absoluta
                        # Isso previne que jogos pequenos influenciem indevidamente
                        peso_influencia = jaccard * intersecao
                        gen = mapa_generos[vizinho]
                        pontuacao_genero[gen] += peso_influencia
            
            if pontuacao_genero:
                # O gênero vencedor é o que acumulou maior peso Jaccard dos vizinhos
                genero_vencedor = max(pontuacao_genero, key=pontuacao_genero.get)
                novos_generos[jogo] = genero_vencedor
                
        # Atualiza a base de conhecimento consolidada
        for jogo, gen in novos_generos.items():
            mapa_generos[jogo] = gen
            macro_generos[jogo] = agrupar_macro_generos(gen)
            jogos_nao_classificados.remove(jogo)
            
    # Para qualquer jogo que tenha ficado isolado, colocamos como "Desconhecido/Casual"
    for jogo in jogos_nao_classificados:
        mapa_generos[jogo] = "Casual/Isolado"
        macro_generos[jogo] = "Outros"

    return mapa_generos, macro_generos, total_jogadores

# ── ETAPA 3: CLASSIFICAÇÃO DOS JOGADORES ──────────────────────────────────
def classificar_perfis_jogadores(usuarios, macro_generos):
    """
    Analisa as horas gastas em cada macro-gênero e define um "Label" 
    comportamental descritivo para o jogador (Ex: Híbrido, Focado, Casual).
    """
    perfis_estatisticas = defaultdict(list)
    
    for user, jogos_dict in usuarios.items():
        horas_por_genero = defaultdict(float)
        horas_totais = 0.0
        
        for jogo, horas in jogos_dict.items():
            # Conta horas jogadas se disponíveis (assumindo que o CSV tem valores de horas > 0)
            if horas > 0:
                gen = macro_generos.get(jogo, "Outros")
                horas_por_genero[gen] += horas
                horas_totais += horas
                
        if horas_totais == 0:
            continue
            
        # Ordenar os gêneros do usuário pelas horas gastas
        generos_ordenados = sorted(horas_por_genero.items(), key=lambda x: x[1], reverse=True)
        
        gen_1, horas_1 = generos_ordenados[0]
        perc_1 = horas_1 / horas_totais
        
        # Regras Heurísticas para Rotular o Jogador Baseado nos Dados
        if perc_1 >= 0.65:
            # Mais de 65% do tempo gasto em apenas um gênero
            perfil = f"Especialista em {gen_1}"
        elif len(generos_ordenados) >= 2:
            gen_2, horas_2 = generos_ordenados[1]
            perc_2 = horas_2 / horas_totais
            if (perc_1 + perc_2) >= 0.75 and perc_2 >= 0.20:
                # Dois gêneros dominam 75% do tempo
                perfil = f"Híbrido ({gen_1} + {gen_2})"
            else:
                perfil = "Multigênero Eclético"
        else:
            perfil = "Multigênero Eclético"
            
        perfis_estatisticas[perfil].append({
            'user': user,
            'horas_totais': horas_totais,
            'gen_principal': gen_1
        })
        
    return perfis_estatisticas

# ── ETAPA 4: ESTATÍSTICAS E VISUALIZAÇÃO ──────────────────────────────────
def visualizar_analise_semantica(macro_generos, perfis_estatisticas, total_jogadores):
    """
    Gera um dashboard resumindo os resultados semânticos.
    """
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    fig.canvas.manager.set_window_title("Análise Semântica de Gêneros e Perfis")
    
    # ── Gráfico 1: População de Jogos por Macro-Gênero ──
    ax_pie = axs[0]
    contagem_macro = defaultdict(int)
    for jogo, gen in macro_generos.items():
        contagem_macro[gen] += 1
        
    # Filtrar pequenos para "Outros" para não poluir
    pie_labels = []
    pie_sizes = []
    for gen, count in contagem_macro.items():
        if count > 50:
            pie_labels.append(gen)
            pie_sizes.append(count)
            
    ax_pie.pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax_pie.set_title("Distribuição do Catálogo da Steam por Gênero\n(Sementes + Jaccard Propagation)", fontweight='bold')

    # ── Gráfico 2: Perfis Comportamentais dos Jogadores ──
    ax_bar = axs[1]
    
    # Agregar contagens dos perfis identificados
    contagem_perfis = {p: len(users) for p, users in perfis_estatisticas.items() if len(users) > 30}
    # Ordenar pelos mais comuns
    perfis_ordenados = sorted(contagem_perfis.items(), key=lambda x: x[1], reverse=True)[:10]
    
    nomes = [p[0] for p in perfis_ordenados]
    valores = [p[1] for p in perfis_ordenados]
    
    bars = ax_bar.barh(nomes, valores, color='#2ecc71', edgecolor='#27ae60')
    ax_bar.set_title("Identificação de Perfis de Jogadores", fontweight='bold')
    ax_bar.set_xlabel("Quantidade de Jogadores")
    ax_bar.invert_yaxis()  # O maior fica no topo
    ax_bar.grid(axis='x', linestyle='--', alpha=0.6)
    
    for bar in bars:
        width = bar.get_width()
        ax_bar.text(width + 10, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                    ha='left', va='center', fontweight='bold', fontsize=9)
                    
    plt.tight_layout()
    plt.show()

def executar_analise_comportamental(usuarios, adj):
    """
    Ponto de entrada do módulo. Substitui o antigo agrupamento Louvain
    por um Pipeline completo de Data Enrichment (Taxonomia) -> ML de Grafos
    (Label Propagation / Jaccard) -> Feature Engineering (Perfis).
    """
    print("\n" + "="*70)
    print("🧬 INICIANDO CLASSIFICAÇÃO SEMÂNTICA E PROPAGAÇÃO (JACCARD)".center(70))
    print("="*70)
    
    print(f"[1/4] Inicializando Taxonomia Âncora ({len(ANCORAS_GENERO)} jogos)...")
    
    print("[2/4] Calculando Similaridade de Jaccard e Propagando Gêneros no Grafo...")
    mapa_generos, macro_generos, total_jogadores = calcular_jaccard_e_propagar_generos(usuarios, adj)
    print(f"      - {len(mapa_generos)} jogos classificados com sucesso pela comunidade.")
    
    print("[3/4] Avaliando bibliotecas e classificando perfis de jogadores...")
    perfis_estatisticas = classificar_perfis_jogadores(usuarios, macro_generos)
    
    print("[4/4] Resultados e Perfis Identificados:\n")
    
    # Exibir um resumo dos maiores grupos encontrados
    ordenados_por_tamanho = sorted(perfis_estatisticas.items(), key=lambda x: len(x[1]), reverse=True)
    
    for perfil, lista_users in ordenados_por_tamanho[:7]:
        print(f"🔹 {perfil}: {len(lista_users)} jogadores")
        # Mostrar exemplo de um jogador do grupo e suas horas
        exemplo = lista_users[0]
        print(f"   Ex: Jogador ID {exemplo['user']} (Total: {exemplo['horas_totais']:.1f} horas)")
        print("-" * 70)
        
    print("\n[!] Renderizando Dashboard de Classificação Semântica...")
    visualizar_analise_semantica(macro_generos, perfis_estatisticas, total_jogadores)
