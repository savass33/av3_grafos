# Projeto Final AV3 - Grafos: Ecossistema e Comunidades da Steam

Este projeto utiliza a **Teoria dos Grafos** para modelar, analisar e visualizar o comportamento de jogadores na plataforma Steam. A partir de um dataset real, o sistema constrói uma rede complexa onde jogos são conectados pela interseção de suas bases de jogadores, permitindo análises de caminhos mínimos, propagação semântica de gêneros e descoberta de perfis comportamentais.

## 🛠️ Pré-requisitos e Configuração do Ambiente

O projeto possui visualizações gráficas interativas nativas do Python. Para que elas funcionem corretamente, é estritamente necessário ter o pacote **Tkinter** instalado no seu Sistema Operacional, além das bibliotecas do Python.

### Passo 1: Instalar dependência gráfica no Sistema Operacional (Apenas Linux)
Se você estiver utilizando Linux, instale o pacote `tk` antes de rodar o código.
* **Ubuntu / Debian / Mint:** `sudo apt-get install python3-tk`
* **Arch Linux / Manjaro:** `sudo pacman -S tk`
* **Fedora:** `sudo dnf install python3-tkinter`
*(No Windows e macOS, o Tkinter já costuma vir embutido na instalação padrão do Python).*

### Passo 2: Criar e Ativar a Virtual Environment (Recomendado)
No terminal, dentro da pasta do projeto, execute:
```bash
# 1. Criar a VENV
python3 -m venv venv

# 2. Ativar a VENV
# No Linux/macOS:
source venv/bin/activate
# No Windows (CMD):
venv\Scripts\activate.bat
# No Windows (PowerShell):
venv\Scripts\Activate.ps1
```

### Passo 3: Instalar as bibliotecas Python
Com a VENV ativada, instale os pacotes definidos no `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 🚀 Como Executar o Projeto

No terminal, com a venv ativada, rode o arquivo principal:
```bash
python main.py
```

### 🧠 A Matemática por trás das Análises (Para Avaliação)
O projeto atende à exigência de "Análises de Comunidades e Clusters" utilizando duas matemáticas principais aplicadas ao grafo:

1. **Descoberta de Gêneros de Jogos (Índice de Jaccard):**
   Como o CSV não tem gêneros, usamos **Label Propagation**. O algoritmo calcula a Similaridade de Jaccard entre comunidades de jogos: `|A ∩ B| / (|A| + |B| - |A ∩ B|)`. Se o Jogo A (desconhecido) tem público quase idêntico ao Jogo B (ex: CS:GO = Shooter), a similaridade fica altíssima e o Jogo A herda o gênero "Shooter". Isso classifica todo o catálogo autonomamente.

2. **Perfis Comportamentais de Jogadores (Proporção de Horas):**
   Com os jogos classificados, o sistema varre o histórico do usuário e avalia suas horas em porcentagem:
   * **Especialista:** Gasta **> 65%** do tempo total em um único gênero.
   * **Híbrido:** Gasta **> 75%** do tempo dividido entre dois gêneros específicos.
   * **Eclético:** Horas pulverizadas em 3 ou mais categorias diferentes.

### 🖥️ Entendendo o Fluxo de Execução Visual
O programa roda sequencialmente e executa as seguintes etapas:
1. **Terminal:** Carrega o dataset, constrói o grafo ponderado e exibe os resultados dos algoritmos clássicos (**BFS, DFS e Dijkstra**).
2. **Terminal:** Executa a propagação semântica de gêneros (Índice de Jaccard) e imprime os perfis de jogadores.
3. **Interface Gráfica 1 (Dashboard de Perfis):** Uma janela do Matplotlib abrirá mostrando as estatísticas de gêneros e as tribos de jogadores. 
   * ⚠️ **Atenção:** O programa ficará "pausado" nesta tela. **Feche a janela** (clique no 'X') para continuar.
4. **Interface Gráfica 2 (Visualização do Grafo):** Assim que a primeira janela for fechada, a visualização estrutural da rede (NetworkX) abrirá. Você pode dar Zoom, Pan e passar o mouse sobre os nós (Tooltip) para ver estatísticas de afinidade e o trajeto do caminho mínimo do algoritmo Dijkstra.

## 📁 Estrutura de Arquivos
* `main.py`: Orquestrador principal responsável por unir os dados, os algoritmos e a visualização.
* `grafo.py`: Módulo responsável pela leitura do dataset (CSV) e construção da lista de adjacências.
* `bfs.py` e `dfs.py`: Implementação pura das Buscas em Largura e Profundidade.
* `dijkstra.py`: Implementação do Caminho Mínimo, otimizada com cálculo inversamente proporcional ao peso da aresta.
* `analise_jogadores.py`: Inteligência do projeto. Usa similaridade de Jaccard e propagação de rótulos para deduzir gêneros de jogos e perfilar os usuários.
* `visualizacao.py`: Renderizador interativo da topologia da rede e do resultado do Dijkstra.
* `RELATORIO.md`: Documentação técnica e teórica exigida para avaliação.
* `steam-200k.csv`: Dataset original de entrada.# av3_grafos
