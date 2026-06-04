from grafo import carregar_dados, construir_grafo
from bfs import bfs
from dfs import dfs
from dijkstra import dijkstra
from visualizacao import renderizar_interface
from analise_jogadores import executar_analise_comportamental


if __name__ == '__main__':
    print("Carregando dados...")
    usuarios = carregar_dados('steam-200k.csv')
    print(f"Sucesso: {len(usuarios)} usuarios carregados.")

    print("Construindo grafo...")
    adj = construir_grafo(usuarios)
    total_nos = len(adj)
    total_arestas = sum(len(v) for v in adj.values()) // 2
    print(f"Grafo pronto: {total_nos} jogos, {total_arestas} arestas.")

    jogo_a = "The Elder Scrolls V Skyrim"
    jogo_b = "Eldevin"

    # ── BFS ──────────────────────────────────────────────────────────────────
    print(f"\n=== BFS a partir de '{jogo_a}' ===")
    dist_bfs = bfs(adj, jogo_a)
    vizinhos_diretos = sorted(
        [(j, adj[jogo_a][j]) for j in adj[jogo_a]],
        key=lambda x: x[1], reverse=True
    )[:10]
    print(f"Jogos alcancaveis: {len(dist_bfs)}")

    # ── DFS ──────────────────────────────────────────────────────────────────
    print(f"\n=== DFS a partir de '{jogo_a}' ===")
    ordem_dfs = dfs(adj, jogo_a)
    print(f"Jogos visitados: {len(ordem_dfs)}")

    # ── Dijkstra ─────────────────────────────────────────────────────────────
    print(f"\n=== Dijkstra: '{jogo_a}' -> '{jogo_b}' ===")
    custo, caminho = dijkstra(adj, jogo_a, jogo_b)
    if caminho:
        print(f"Caminho encontrado com custo {custo:.4f}")
    else:
        print("Sem caminho encontrado.")

    # ── Analise de Perfis e Grupos ───────────────────────────────────────────
    executar_analise_comportamental(usuarios, adj)

    # ── Visualização Gráfica do Grafo ────────────────────────────────────────
    renderizar_interface(adj, jogo_origem=jogo_a, jogo_destino=jogo_b, caminho_otimo=caminho)
