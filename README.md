## 🎓 Informações Acadêmicas

*   **Instituição:** Universidade de Fortaleza (UNIFOR)
*   **Disciplina:** Resolução de Problemas com Grafos
*   **Turma:** T290-60 (T24CD)
*   **Professor:** Matheus Ferreira

### 👥 Membros da Equipe
*   **Savas Neto** - 2410432
*   **Anderson Viana** - 2410492
*   **Paulo Alencar** - 2416507


## 🎮 Steam Ecosystem & Community Analysis (Graph Theory)

Este projeto utiliza a **Teoria dos Grafos** para modelar, analisar e visualizar a complexa rede de afinidade entre jogos e o comportamento dos jogadores na plataforma Steam. Através de um dataset real de 200k registros, o sistema constrói uma malha onde jogos são conectados pela interseção de suas bases de usuários, permitindo a descoberta autônoma de gêneros e perfis comportamentais.

---

## 🚀 Funcionalidades Principais

*   **Modelagem de Redes Reais:** Construção de um grafo massivo com mais de 3.500 nós e 840.000 arestas.
*   **Buscas Clássicas (BFS/DFS):** Exploração de conectividade e nichos de mercado.
*   **Caminho Mínimo Otimizado (Dijkstra):** Algoritmo adaptado para encontrar rotas de maior afinidade semântica.
*   **Classificação por Label Propagation:** Dedução automática de gêneros de jogos via **Índice de Jaccard**.
*   **Profiling de Usuários:** Agrupamento de jogadores em tribos (Especialista, Híbrido, Eclético) com base na heurística de horas jogadas.
*   **Visualização Interativa:** Dashboard de estatísticas e renderização topológica da rede com NetworkX.

---

## 🛠️ Configuração do Ambiente

### 1. Dependências do Sistema (Interface Gráfica)
O projeto utiliza o **Tkinter** para as janelas interativas.

*   **Linux:**
    ```bash
    sudo apt-get install python3-tk  # Ubuntu/Debian
    sudo dnf install python3-tkinter # Fedora
    ```
*   **macOS:** Geralmente embutido. Se necessário, use `brew install python-tk`.
*   **Windows:** Embutido na instalação padrão do Python (certifique-se de que "tcl/tk and IDLE" estava marcado no instalador).

### 2. Instalação
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
# No Linux/macOS:
source venv/bin/activate
# No Windows (Command Prompt):
venv\Scripts\activate
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 3. Instalar bibliotecas Python
pip install -r requirements.txt
```

### 3. Execução
```bash
python main.py
```

---

## 🧠 Inteligência e Algoritmos

O projeto utiliza uma combinação de algoritmos clássicos e heurísticas modernas para extrair inteligência dos dados:

### 1. Busca em Largura (BFS)
*   **Utilidade:** Utilizada para mapear o **grau de conectividade** a partir de um jogo específico.
*   **Aplicação:** Identifica todos os jogos alcançáveis e os organiza por "nível de amizade" (distância), permitindo descobrir até onde a influência de um título se estende na rede.

### 2. Busca em Profundidade (DFS)
*   **Utilidade:** Utilizada para explorar **nichos e ramificações profundas** da rede.
*   **Aplicação:** Útil para detectar caminhos que levam a comunidades menores ou jogos menos populares ("long tail"), explorando uma linha de afinidade até o seu limite.

### 3. Algoritmo de Dijkstra (Caminho Mínimo)
*   **Utilidade:** Encontrar a **rota de maior afinidade** entre dois jogos distantes.
*   **Truque Matemático:** Como o Dijkstra busca o *menor* custo, mas nós queremos a *maior* afinidade (peso), transformamos o peso da aresta em `Custo = 1.0 / Peso`.
*   **Aplicação:** Traça o "caminho lógico" que um jogador percorreria entre gêneros diferentes (ex: de um RPG denso para um Shooter casual) através de jogos que servem como "pontes" de público.

### 4. Similaridade de Jaccard
*   **Utilidade:** Medir a **proximidade estatística** entre duas bases de jogadores.
*   **Fórmula:** `J = |A ∩ B| / |A ∪ B|`.
*   **Aplicação:** Define se o público de um jogo "X" é o mesmo de um jogo "Y". É a métrica base para decidir se um jogo deve herdar o gênero de seu vizinho.

### 5. Label Propagation (Propagação de Rótulos)
*   **Utilidade:** **Classificação autônoma** de milhares de jogos sem metadados.
*   **Aplicação:** Começando por 50 jogos conhecidos ("âncoras"), o algoritmo "infecta" os vizinhos desconhecidos com o gênero predominante, baseando-se na força da similaridade de Jaccard.

### 6. Heurística de Perfis Comportamentais
*   **Utilidade:** Agrupar usuários em **tribos comportamentais**.
*   **Aplicação:** Analisa as horas totais e a distribuição de gêneros para classificar o jogador como:
    *   **Especialista:** > 65% das horas em um único gênero.
    *   **Híbrido:** > 75% das horas divididas entre dois gêneros principais.
    *   **Eclético:** Horas pulverizadas em 3 ou mais categorias.

---

## 📂 Estrutura do Projeto

*   `main.py`: Orquestrador principal do fluxo de execução.
*   `grafo.py`: Módulo de processamento de dados e construção da lista de adjacências.
*   `bfs.py`, `dfs.py`, `dijkstra.py`: Implementações puras dos algoritmos de grafos.
*   `analise_jogadores.py`: Núcleo de inteligência de dados (Jaccard e Perfis).
*   `visualizacao.py`: Renderizador gráfico e dashboard.
*   `find_path.py`: Script auxiliar para descoberta de rotas longas entre comunidades.
*   `RELATORIO.md`: Documentação técnica detalhada para avaliação acadêmica.

---

## 📊 Resultados Alcançados
*   **Processamento Eficiente:** Manipulação de uma rede com **3.577 vértices** e **841.388 arestas**.
*   **Precisão de Gêneros:** Categorização autônoma de ~3.400 jogos com alta coerência semântica.
*   **Identificação de Clusters:** Visualização clara da formação de comunidades (ex: Shooters, RPGs, Indie) baseada puramente em comportamento de consumo.