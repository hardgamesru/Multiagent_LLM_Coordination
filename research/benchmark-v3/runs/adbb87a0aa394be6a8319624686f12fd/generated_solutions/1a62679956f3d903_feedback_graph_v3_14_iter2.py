from typing import Dict, List
import networkx as nx

def strongly_connected(graph: Dict[str, List[str]]) -> List[List[str]]:
    g = nx.DiGraph()
    g.add_edges_from((u, v) for u, vs in graph.items() for v in vs)
    
    # Найти компоненты сильной связности
    sccs = [sorted(list(c)) for c in nx.algorithms.StronglyConnectedComponents(g)]
    
    # Отсортировать компоненты лексикографически
    return sorted(sccs)
