import networkx as nx
import pandas as pd
import numpy as np

def create_graph_from_calendar(calendar) -> nx.Graph:
    """ Creates an adjaceny matrix 
    
    Parameters:
        calendar: Calendar object, must contain courses
    """
    n = sum(course.number_of_groups() for course in calendar.courses.values())
    cols = sum([
        [
            course_title + "---" + group
            for group in course.groups
        ] for course_title, course in calendar.courses.items()
    ], [])
    adj_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols, dtype=int)
    
    # add edges between 'layers' in adj matrix
    for course in calendar.courses:
        adj_matrix.loc[adj_matrix.index.str.startswith(course), ~adj_matrix.columns.str.startswith(course)] = 1
    
    return nx.from_pandas_adjacency(adj_matrix, create_using=nx.Graph())


def remove_edges_overlapping(G: nx.Graph, calendar) -> None:
    """ Remove edges between overlapping practical lectures """
    for node in G:
        course, group = node.split("---")

        neighbors = pd.DataFrame(
            pd.Series(G.neighbors(node))\
                .map(lambda x: x.split("---"))\
                .to_list()
        ).rename(columns={0: "course", 1: "group"})
        
        for _, row in neighbors.iterrows():
            overlap = calendar.courses[course]\
                        .groups[group]\
                        .overlaps_with_course(calendar, row["course"], row["group"])
            if overlap: 
                G.remove_edge(node, f"{row['course']}---{row['group']}")
                
    G.remove_nodes_from(list(nx.isolates(G)))


def get_lecture_combinations(G: nx.Graph, calendar) -> pd.DataFrame:
    """ Finds all possible combinations of practical lectures without 
    overlapping lectures
    
    Each practical lecture is connected to every other practical lecture,
    except the ones of the same course. After removing edges of overlapping
    lectures we can search for cliques of size equal to the number of subjects.
    Each clique is a possible combination
    """
    cal_size = calendar.number_of_courses()
    combis = np.array([
        clique 
        for clique in nx.find_cliques(G) 
        if len(clique) == cal_size
    ])

    # case: no combinations that do not overlap
    if len(combis) == 0:
        return pd.DataFrame(data=[], columns=sorted(calendar.list_courses()))

    combis.sort(axis=1)
    return pd.DataFrame(data=combis, columns=sorted(calendar.list_courses()))


def search_by_cliques(calendar) -> pd.DataFrame:
    """ wraps all functions for clique based search """
    G = create_graph_from_calendar(calendar)
    remove_edges_overlapping(G, calendar)
    return get_lecture_combinations(G, calendar)
