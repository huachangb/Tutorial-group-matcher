import numpy as np
import pandas as pd
import networkx as nx

def create_graph_from_calendar(calendar) -> nx.Graph:
    """ Creates an adjaceny matrix 
    
    Parameters:
        calendar: Calendar object, must contain courses
    """
    n = sum(len(course) for course in calendar.courses.values())
    cols = sum([
        [
            course_title + "---" + practical.group 
            for practical in course.practical_lectures.values()
        ] for course_title, course in calendar.courses.items()
    ], [])
    adj_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols, dtype=int)
    hierarchy = calendar.list_courses()
    
    # add edges between 'layers' in adj matrix
    for i in range(len(hierarchy)):
        course = hierarchy[i]
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
                        .practical_lectures[group]\
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
    cal_size = len(calendar)
    combis = np.array([
        clique 
        for clique in nx.find_cliques(G) 
        if len(clique) == cal_size
    ])
    combis.sort(axis=1)
    return pd.DataFrame(data=combis, columns=sorted(calendar.list_courses()))
