from grafo import carregar_dados, construir_grafo
from dijkstra import dijkstra

usuarios = carregar_dados('steam-200k.csv')
adj = construir_grafo(usuarios)

jogo_a = "The Elder Scrolls V Skyrim"
print(f"Buscando caminhos longos a partir de {jogo_a}...")

encontrado = False
for jogo_b in adj:
    if jogo_b != jogo_a:
        custo, caminho = dijkstra(adj, jogo_a, jogo_b)
        if caminho and len(caminho) >= 5 and len(caminho) <= 7:
            print(f"Sucesso! {jogo_a} -> {jogo_b}")
            print(f"Custo: {custo}, Caminho: {' -> '.join(caminho)}")
            encontrado = True
            break

if not encontrado:
    print("Nenhum caminho com 4-6 nós encontrado. Tentando len >= 3")
    for jogo_b in adj:
        if jogo_b != jogo_a:
            custo, caminho = dijkstra(adj, jogo_a, jogo_b)
            if caminho and len(caminho) >= 3:
                print(f"Sucesso! {jogo_a} -> {jogo_b}")
                print(f"Custo: {custo}, Caminho: {' -> '.join(caminho)}")
                break
