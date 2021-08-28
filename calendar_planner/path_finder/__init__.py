import numpy as np
import pandas as pd
import networkx as nx
import re
from networkx.drawing.nx_agraph import graphviz_layout
from itertools import product, permutations

def create_graph_from_calendar(calendar) -> nx.Graph:
    """ Creates an adjaceny matrix 
    
    Parameters:
        calendar: Calendar object, must contain courses
    """
    # create adjacency matrix
    n = sum(len(course) for course in calendar.courses.values())
    cols = sum([
        [course_title + "---" + practical.group for practical in course.practical_lectures.values()] 
            for course_title, course in calendar.courses.items()
    ], [])
    adj_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols, dtype=int)
    
    hierarchy = calendar.list_courses()
    
    # add edges between 'layers' in adj matrix
    for i in range(len(hierarchy)):
        course = hierarchy[i]
        adj_matrix.loc[adj_matrix.index.str.startswith(course), ~adj_matrix.columns.str.startswith(course)] = 1
        
    return nx.from_pandas_adjacency(adj_matrix, create_using=nx.Graph())


def draw_as_nn(G: nx.Graph, with_labels=False) -> None:
    """ Draws graph in neural network format """
    pos = graphviz_layout(G, prog='dot', args="-Grankdir=LR")
    nx.draw(G,with_labels=with_labels,pos=pos)


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
                G.remove_edge(node, f"{row['course']}---{row['group']}")
                # remove_edges.append((node, row["course"] + "---" + row["group"]))
                
    # G.remove_edges_from(remove_edges)
    G.remove_nodes_from(list(nx.isolates(G)))



def get_lecture_combinations(G: nx.Graph, calendar) -> list:
    cal_size = len(calendar)
    combis = np.array([
        clique 
        for clique in nx.find_cliques(G) 
        if len(clique) == cal_size
    ])
    combis.sort(axis=1)
    return pd.DataFrame(data=combis, columns=sorted(calendar.list_courses()))


def get_lecture_combinations2(calendar):
    G = create_graph_from_calendar(calendar)
    remove_edges_overlapping(G, calendar)
    return get_lecture_combinations(G, calendar)
