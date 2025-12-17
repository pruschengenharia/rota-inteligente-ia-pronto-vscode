# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

Disciplina: Artificial Intelligence Fundamentals  
Projeto: Otimização de Rotas e Zonas de Entrega — Sabor Express  
Linguagem: Python  
Paradigmas: Busca em grafos + Aprendizado não supervisionado (clustering)

---

## 1. Descrição do problema, desafio proposto e objetivos

### 1.1 Contexto do problema
A Sabor Express (delivery local) enfrenta atrasos e rotas ineficientes em horários de pico. O problema central é determinar rotas de menor custo entre pontos de interesse (centro de distribuição e destinos) em uma cidade modelada como grafo, considerando diferentes métricas (distância e tempo).

Durante alta demanda, há aumento no volume de entregas, e torna-se necessário agrupar entregas próximas para formar zonas de atendimento, reduzindo deslocamentos redundantes e melhorando a alocação de entregadores.

### 1.2 Desafio proposto
Construir uma solução que:
- Modele o ambiente urbano como um grafo ponderado (nós e arestas com custos).
- Compare algoritmos clássicos de busca (BFS, DFS, A*).
- Execute K-Means para agrupar entregas por proximidade.
- Gere artefatos visuais (diagrama do grafo e mapa de clusters) para apoiar análise.

### 1.3 Objetivos

#### 1.3.1 Objetivo geral
Otimizar entregas reduzindo custo (distância/tempo) e aumentando previsibilidade e eficiência operacional.

#### 1.3.2 Objetivos específicos
- Carregar nós e arestas a partir de CSV e construir o grafo com NetworkX.
- Comparar BFS, DFS e A* no trajeto start → goal.
- Medir custo do caminho (por métrica) e tempo de execução (ms).
- Executar K-Means em coordenadas (x, y) das entregas e gerar o gráfico de clusters.
- Exportar o grafo como imagem (docs/grafo.png) e, quando possível, como DOT (docs/grafo.dot).

---

## 2. Explicação detalhada da abordagem adotada

A solução implementa um pipeline único executado via linha de comando (CLI), orquestrado por src/main.py.

### 2.1 Carregamento do grafo
- Lê data/nodes.csv e data/edges.csv.
- Cria um grafo não-direcionado (nx.Graph) com atributos por nó e por aresta:
  - Nó: id, label, type, x, y
  - Aresta: distance_km, time_min

Arquivo: src/graph_loader.py

### 2.2 Geração de visualizações
- Desenha o grafo com posições reais (x, y) e rotula arestas com distância.
- Exporta arquivo .dot (Graphviz) se o ambiente suportar.

Arquivos: src/plot_graph.py  
Saídas:
- docs/grafo.png
- docs/grafo.dot (opcional)

### 2.3 Comparação de algoritmos de busca
- Executa BFS, DFS e A* para encontrar caminho entre --start e --goal.
- Calcula custo total somando o atributo por aresta definido por --metric:
  - distance_km (distância em km)
  - time_min (tempo em minutos)
- Registra tempo de execução em ms com time.perf_counter() e imprime ranking.

Arquivos: src/evaluate.py e src/search_algorithms.py

### 2.4 Clusterização com K-Means
- Carrega data/deliveries.csv com coordenadas das entregas.
- Executa K-Means com k clusters, gerando zonas de entrega.
- Plota clusters e centróides e salva em docs/.

Arquivos: src/clustering.py e src/main.py  
Saída:
- docs/kmeans_clusters.png

### 2.5 Saídas consolidadas
- Console: tabela comparativa de algoritmos + resumo do K-Means.
- Pasta docs/: imagens e arquivos de apoio para relatório/entrega.

---

## 3. Algoritmos utilizados

### 3.1 BFS (Breadth-First Search)
- O que faz: busca em largura; encontra caminho com menor número de arestas em grafos não ponderados.
- Como foi aplicado: fila (deque), conjunto de visitados e mapeamento de pais para reconstrução do caminho.
- Limitação: não otimiza distância/tempo em grafos ponderados.

Arquivo: src/search_algorithms.py (bfs_path)

### 3.2 DFS (Depth-First Search)
- O que faz: busca em profundidade; explora um caminho até o fim antes de retroceder.
- Como foi aplicado: pilha, conjunto de visitados e pais.
- Limitação: não garante caminho de menor custo e pode retornar solução subótima.

Arquivo: src/search_algorithms.py (dfs_path)

### 3.3 A* (A-Star)
- O que faz: encontra caminho de menor custo combinando:
  - custo acumulado g(n) (peso real pelas arestas)
  - heurística h(n) (estimativa até o objetivo)
- Heurística adotada: distância euclidiana entre coordenadas (x, y) do nó atual e do nó objetivo.
- Como foi aplicado: fila de prioridade (heapq) com f(n) = g(n) + h(n) e conjunto closed.

Arquivo: src/search_algorithms.py (astar_path)

### 3.4 K-Means Clustering
- O que faz: agrupa entregas próximas em k clusters para formar zonas de atendimento.
- Entrada: coordenadas (x, y) do deliveries.csv.
- Saídas: cluster por entrega, centróides e inércia (medida de compactação interna dos clusters).

Arquivo: src/clustering.py (run_kmeans)

---

## 4. Diagrama do grafo/modelo usado na solução

O diagrama do grafo é gerado automaticamente por código e salvo em:
- docs/grafo.png — visualização estática do grafo com nós, arestas e distâncias
- docs/grafo.dot — exportação em formato DOT (quando disponível, para uso em Graphviz)

### 4.1 Como gerar o diagrama
Ao rodar o projeto, ele executa automaticamente:
- plot_graph(G) → gera docs/grafo.png
- export_graphviz_dot(G) → tenta gerar docs/grafo.dot

---

## 5. Análise dos resultados, eficiência da solução, limitações e sugestões de melhoria

### 5.1 Resultados (como interpretar)
O projeto imprime uma tabela comparando BFS, DFS e A* com:
- Caminho encontrado (ex.: A → ... → F)
- Custo total (por distance_km ou time_min)
- Tempo de execução em milissegundos

Interpretação esperada em grafos ponderados:
- BFS tende a minimizar número de arestas, mas pode não minimizar custo.
- DFS pode ser rápido, porém frequentemente retorna caminhos subótimos.
- A* tende a fornecer melhor custo quando a heurística é coerente com o problema (coordenadas espaciais ajudam).

Na etapa de K-Means, o projeto produz:
- Imagem docs/kmeans_clusters.png
- Listagem de entregas por cluster e a inércia do modelo.

### 5.2 Eficiência (visão prática)
- BFS/DFS: tipicamente O(V + E) para exploração.
- A*: depende da heurística; pode reduzir busca vs. algoritmos cegos.
- K-Means: custo aproximado O(n * k * i), com n entregas e i iterações.

O projeto mede tempo real em ms para comparação empírica.

### 5.3 Limitações
- Grafo não-direcionado: vias reais podem ser mão única; o modelo atual usa nx.Graph().
- BFS/DFS não consideram pesos: servem como baseline, mas não otimizam distância/tempo.
- Heurística do A*: euclidiana; se a métrica for tempo com trânsito real, pode haver divergências.
- K-Means usa apenas (x, y): não considera prioridade, janela de tempo, volume/peso, capacidade do entregador.
- Exportação DOT pode falhar silenciosamente: depende de pydot/graphviz no ambiente.

### 5.4 Sugestões de melhoria
- Usar grafo direcionado (nx.DiGraph) para modelar sentidos de vias.
- Implementar Dijkstra como baseline ótimo para grafos ponderados (sem heurística).
- Evoluir para múltiplos destinos (roteirização) com VRP/TSP heurístico.
- Enriquecer clusterização com atributos (prioridade, tempo, tipo de entrega, capacidade).
- Escolher k com método do cotovelo (Elbow) e/ou Silhouette Score.
- Salvar relatórios em CSV/JSON para reprodução e auditoria.

---

## 6. Como executar

### 6.1 Instalar dependências
pip install -r requirements.txt

### 6.2 Executar pipeline completo (exemplos)
Distância como métrica e 2 clusters:
python -m src.main --start A --goal F --metric distance_km --k 2

Tempo como métrica e 3 clusters:
python -m src.main --start A --goal F --metric time_min --k 3

### 6.3 Resultados gerados
- docs/grafo.png — diagrama do grafo
- docs/grafo.dot — arquivo DOT (opcional)
- docs/kmeans_clusters.png — clusters de entregas
- Terminal — comparação BFS/DFS/A* e resumo do K-Means

---

## 7. Estrutura do repositório

rota-inteligente-ia/
├── README.md
├── requirements.txt
├── data/
│   ├── nodes.csv
│   ├── edges.csv
│   └── deliveries.csv
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── graph_loader.py
│   ├── plot_graph.py
│   ├── evaluate.py
│   ├── search_algorithms.py
│   └── clustering.py
└── docs/
    ├── grafo.png
    ├── grafo.dot
    └── kmeans_clusters.png

