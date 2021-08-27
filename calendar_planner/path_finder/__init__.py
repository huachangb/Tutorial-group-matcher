import numpy as np
import pandas as pd
import networkx as nx
import re
from networkx.drawing.nx_agraph import graphviz_layout

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
    for i in range(len(hierarchy) - 1):
        first_layer = hierarchy[i]
        second_layer = hierarchy[i + 1]
        adj_matrix.loc[adj_matrix.index.str.startswith(first_layer), 
                       adj_matrix.columns.str.startswith(second_layer)] = 1
        
    return nx.from_pandas_adjacency(adj_matrix, create_using=nx.DiGraph())


def draw_as_nn(G: nx.Graph, labels=False) -> None:
    """ Draws graph in neural network format """
    pos = graphviz_layout(G, prog='dot', args="-Grankdir=LR")
    nx.draw(G,with_labels=labels,pos=pos)


