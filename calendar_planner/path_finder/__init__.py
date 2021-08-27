import numpy as np
import pandas as pd
import networkx as nx
import re
from networkx.drawing.nx_agraph import graphviz_layout
from itertools import product, permutations

def create_graph_from_calendar(calendar, hierarchy: list) -> nx.Graph:
    """ Creates an adjaceny matrix 
    
    Parameters:
        calendar: Calendar object, must contain courses
        hierarchy: order of 'layers', order does not matter
    """
    # create adjacency matrix
    n = sum(len(course) for course in calendar.courses.values())
    cols = sum([
        [course_title + "---" + practical.group for practical in course.practical_lectures.values()] 
            for course_title, course in calendar.courses.items()
    ], [])
    adj_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols, dtype=int)

    # add edges between 'layers' in adj matrix
    for i in range(len(hierarchy)):
        course = hierarchy[i]
        adj_matrix.loc[adj_matrix.index.str.startswith(course), ~adj_matrix.columns.str.startswith(course)] = 1
        
    return nx.from_pandas_adjacency(adj_matrix, create_using=nx.DiGraph())


def draw_as_nn(G: nx.Graph, labels=False) -> None:
    """ Draws graph in neural network format """
    pos = graphviz_layout(G, prog='dot', args="-Grankdir=LR")
    nx.draw(G,with_labels=labels,pos=pos)


def full_path_count(G: nx.Graph, hierarchy: list) -> int:
    """ Returns the number of full paths """
    source_target = (hierarchy[0], hierarchy[-1])
    sources = []
    targets = []

    for node in G.nodes:
        if re.search(f"^{source_target[0]}", node):
            sources.append(node)
        elif re.search(f"^{source_target[1]}", node):
            targets.append(node)
        
    has_paths = [
        (u, v, has_path) 
            for u, v in product(sources, targets) 
            if (has_path := nx.has_path(G, u, v))
    ]

    return len(has_paths)


###
# 
#   Onderstaande code werkt niet correct - verkeerde aanpak
#
###
def remove_edges_overlapping(G: nx.Graph, calendar) -> None:
    remove_edges = []

    for node in G:
        course, group = node.split("---")
        neighbors = pd.DataFrame(
            pd.Series(G.neighbors(node))\
                .map(lambda x: x.split("---"))\
                .to_list()
        ).rename(columns={0: "course", 1: "group"})
        
        for _, row in neighbors.iterrows():
            overlap = calendar.courses[course]\
                        .practical_lectures[group]\
                        .overlaps_with_course(calendar, row["course"], row["group"])
            if overlap: 
                remove_edges.append((node, row["course"] + "---" + row["group"]))
                
    G.remove_edges_from(remove_edges)
    G.remove_nodes_from(list(nx.isolates(G)))



def brute_force_all(calendar, options):
    """ Bruteforces all permutations of courses """
    for hierarchy in permutations(options, len(options)):
        G = create_graph_from_calendar(calendar, hierarchy)
        remove_edges_overlapping(G, calendar)
        
        if full_path_count(G, hierarchy) > 0:
            return G, hierarchy

    return nx.Graph(), []

