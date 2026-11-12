from typing import Dict, List
import networkx as nx

def strongly_connected(graph: Dict[str, List[str]]) -> List[List[str]]:
    g = nx.DiGraph()
    g.add_edges_from((u,v) for u,neighbors in graph.items() for v in neighbors)
    
    # Find strongly connected components using Tarjan's algorithm
    sccs = list(nx.algorithms.StronglyConnectedComponents(g))
    
    # Convert to sorted node lists and return lex-sorted result
    return sorted([sorted(scc) for scc in sccs])
