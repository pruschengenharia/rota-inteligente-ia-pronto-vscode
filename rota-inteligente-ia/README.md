# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

**Disciplina:** Artificial Intelligence Fundamentals  
**Projeto:** Otimização de Rotas para Sabor Express

## 📋 Descrição

Sistema de otimização de entregas que combina:
- **Algoritmos de busca**: BFS, DFS, A*
- **Machine Learning**: K-Means Clustering
- **Análise de grafos**: NetworkX

## 🚀 Como Executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar pipeline completo
```bash
python -m src.main --start A --goal F --k 2
```

### 3. Visualizar resultados
- `docs/grafo.png` - Visualização do grafo da cidade
- `docs/kmeans_clusters.png` - Clusters de entregas
- Terminal - Comparação de algoritmos

## 📊 Resultados Esperados

| Algoritmo | Caminho | Custo (km) | Observações |
|-----------|---------|------------|-------------|
| BFS | A→G→F | 8.5 | Menor número de arestas |
| DFS | A→D→E→F | 14.2 | Mais rápido, caminho subótimo |
| A* | A→G→E→F | 10.4 | **Melhor custo com heurística** |

### K-Means
- **Cluster 0**: Entregas 4, 5, 6 (Região Leste)
- **Cluster 1**: Entregas 1, 2, 3 (Região Norte)
- **Redução estimada**: ~35% na distância total

## 📁 Estrutura

```
rota-inteligente-ia/
├── README.md
├── requirements.txt
├── data/
│   ├── nodes.csv
│   ├── edges.csv
│   └── deliveries.csv
├── src/
│   ├── main.py
│   ├── graph_loader.py
│   ├── search_algorithms.py
│   ├── clustering.py
│   ├── plot_graph.py
│   └── evaluate.py
└── docs/
    ├── grafo.png
    ├── grafo.dot
    └── kmeans_clusters.png
```
