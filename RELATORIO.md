# Relatório Final - Análise em Grafos (Projeto AV3)

Este documento compila a documentação teórica e técnica da aplicação desenvolvida, em conformidade com as exigências do projeto final de Teoria dos Grafos.

---

## 1. Descrição do Problema
Plataformas de distribuição de jogos, como a Steam, lidam com volumes massivos de usuários e títulos. Um desafio recorrente na ciência de dados aplicada a jogos é: **Como entender a relação e similaridade entre diferentes jogos sem depender de categorias manuais (tags)?** e **Como traçar perfis comportamentais precisos dos usuários baseando-se no ecossistema que eles consomem?**

O problema modelado neste projeto consistiu em mapear o comportamento de mais de 11.000 usuários extraídos de um dataset real da Steam (100k+ registros) para construir um "Grafo de Afinidade". O objetivo foi provar que jogos com sobreposição massiva de jogadores pertencem a gêneros ou comunidades semelhantes, e utilizar algoritmos de grafos para encontrar caminhos entre comunidades distantes, além de classificar automaticamente todo o catálogo utilizando propagação em redes.

---

## 2. Modelagem do Grafo
A escolha da estrutura de dados foi vital para resolver o problema proposto.

* **Vértices (Nós):** Cada vértice no grafo representa um **Jogo** distinto da Steam.
* **Arestas (Links):** Uma aresta é criada entre dois jogos (A e B) se existe **pelo menos um usuário que joga ambos**.
* **Pesos (Ponderação):** O peso de cada aresta é incremental. Ele representa a **Quantidade de Usuários em Comum** entre aqueles dois jogos. Quanto maior o peso, mais forte é a afinidade e proximidade semântica entre os títulos.
* **Características da Rede:** O grafo resultante é Não-Direcionado (a relação de compartilhamento é mútua), Altamente Ponderado, Cíclico (comunidades de jogos se entrelaçam), e apresenta formação evidente de clusters. É uma Rede Real Massiva, superando 3.500 vértices e 841.000 arestas.

A representação em memória foi feita através de um **Dicionário de Adjacências** (`dict` de `dict`), garantindo eficiência `O(1)` na busca de vizinhos e atualização de pesos, algo crucial dado o volume da malha de dados.

---

## 3. Algoritmos Utilizados
O projeto evitou o uso de bibliotecas de "caixa-preta" para os seus núcleos lógicos. Os seguintes algoritmos clássicos de grafos foram programados "do zero":

### 3.1. Busca em Largura (BFS)
Foi implementada utilizando uma estrutura de Fila (`collections.deque`). Sua função no projeto é mapear o grau de conectividade, extraindo os níveis de distância a partir de um "jogo de origem" (ex: *Skyrim*) e retornando os vizinhos classificados pela "força" (peso) da sua conexão, provando quais jogos têm o público mais parecido com a origem.

### 3.2. Busca em Profundidade (DFS)
Implementada de forma iterativa (utilizando uma Pilha, para evitar o limite de recursão do Python em um grafo tão profundo). Ela demonstra a exploração contínua e as ramificações de nicho, indo de um jogo popular até o limite extremo da conectividade da rede.

### 3.3. Algoritmo de Caminho Mínimo (Dijkstra)
Utilizado para encontrar a rota mais barata (ou mais forte) entre dois jogos muito diferentes (ex: *Skyrim* -> *Eldevin*). 
* **O Truque Matemático do Custo:** Em um grafo onde o "Peso" significa "Afinidade", valores altos são "melhores". Como o Dijkstra tradicional busca o *menor* custo acumulado, a modelagem converteu o peso da aresta em um custo topológico: `custo = 1.0 / peso`. Assim, pular entre dois jogos com 300 jogadores em comum é considerado muito mais "barato e rápido" do que pular para um jogo com apenas 1 jogador em comum. O algoritmo se orienta pelos clusters principais do grafo.

### 3.4. Label Propagation e Similaridade de Jaccard (Identificação de Gêneros)
Como o dataset não informa se um jogo é "RPG" ou "FPS", utilizamos Análise em Grafos para deduzir isso matematicamente. Definimos uma base de conhecimento com 50 jogos "âncoras" rotulados manualmente (Ex: CS:GO = Shooter). O algoritmo varre a malha comparando a comunidade de um jogo desconhecido (Jogo X) com seus jogos vizinhos utilizando a **Similaridade de Jaccard**:

> **Fórmula Aplicada:** `Jaccard = |A ∩ B| / (|A| + |B| - |A ∩ B|)`
> *Onde `A` é o total de jogadores do Jogo X, e `B` é o total de jogadores do vizinho.*

Se a interseção de jogadores for muito alta (ex: o público do Jogo X é quase o mesmo do CS:GO), o valor de Jaccard dispara. O algoritmo então "infecta" o jogo desconhecido, copiando o rótulo do seu vizinho mais forte. Isso classifica todo o catálogo da Steam autonomamente.

### 3.5. Classificação Heurística de Perfis (Agrupamento de Usuários)
Com todos os 3.500+ jogos rotulados (graças à etapa 3.4), o sistema calcula o perfil comportamental de cada jogador analisando a distribuição das suas horas jogadas. A matemática funciona por regras de proporção direta:
1. O algoritmo soma `100%` das horas totais do usuário.
2. Agrupa essas horas pelos macro-gêneros recém-descobertos.
3. Aplica as seguintes **Regras Heurísticas de Corte**:
   * **Especialista em [Gênero]:** Se o jogador gasta **> 65%** do seu tempo total em apenas uma categoria.
   * **Híbrido ([Gênero 1] + [Gênero 2]):** Se o tempo do jogador é dividido entre dois gêneros dominantes, onde a soma de ambos seja **>= 75%** das horas totais (e o menor deles tenha pelo menos 20%).
   * **Multigênero Eclético:** Se as horas são pulverizadas em três ou mais categorias, sem atingir os limites de foco acima.

---

## 4. Resultados Obtidos
A infraestrutura rodou com performance otimizada, extraindo os seguintes resultados práticos:
1. **Estruturação Robusta:** Criação dinâmica de **3.577 vértices** associados a **841.388 arestas ponderadas**, sem esgotar os limites da memória devido à eficiência do dicionário de dicionários.
2. **Descoberta de Caminho (Dijkstra):** Encontrada com sucesso a transição lógica entre comunidades de gêneros diferentes, descobrindo o trajeto (*Skyrim -> Team Fortress 2 -> Unturned -> Eldevin*) avaliando os gargalos de afinidade inter-clusters.
3. **Classificação Automática de Jogos:** O modelo `Label Propagation` categorizou de forma autônoma mais de 3.400 jogos desconhecidos baseando-se pura e estritamente na similaridade topológica (Jaccard) do seu público, alcançando agrupamentos extremamente coerentes.
4. **Interfaces Opcionais Interativas:** Geração de Dashboard focado em estatísticas comportamentais, além de um renderizador de Grafo Geométrico (*NetworkX + Matplotlib*) utilizando *Spring Layout* atrelado à gravidade dos pesos.

---

## 5. Interpretação das Análises
A principal conclusão acadêmica derivada das análises aplicadas é que **metadados não são estritamente necessários quando a geometria da rede revela o comportamento**.

Ao utilizarmos algoritmos como o Jaccard Propagation e o BFS com ranking de peso, o grafo demonstrou que o gênero de um jogo emerge naturalmente na forma de **Clusters Fortemente Conectados**. Jogadores da base do CS:GO formaram uma aresta tão grossa com o jogo Team Fortress 2 que o próprio algoritmo enxergou que ambos compartilham do mesmo espaço semântico ("Shooters"). 

Quando aplicamos esses rótulos topológicos nos históricos dos usuários, o sistema foi capaz de ditar perfeitamente o perfil comportamental individual de cada jogador ("Especialista FPS", "Eclético", "Híbrido"), provando que um grafo é uma ferramenta poderosa não apenas para traçar "Rotas de GPS", mas para Inteligência de Mercado e Filtros Colaborativos Estratégicos.