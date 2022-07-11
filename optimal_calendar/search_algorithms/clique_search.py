"""
TODO:
- add support for custom events
"""

import networkx as nx
import pandas as pd
from itertools import combinations


def find_cliques_cal(cal) -> nx.Graph:
    """ 
    Creates graph from calendar such that all practical seminar groups
    are nodes and there exists an edge between two nodes iff
    they do not overlap. 
    """
    # get all practical seminar groups
    practical_seminar_groups = []

    for course_title, course in cal.courses.items():
        course_groups = map(lambda x: (course_title, x), course.practical_seminars.keys())
        practical_seminar_groups = [*practical_seminar_groups, *course_groups]
    
    G = nx.Graph()
    G.add_nodes_from(practical_seminar_groups)

    # add edges
    courses = cal.courses
    seminar_combinations = filter(
        lambda comb: comb[0][0] != comb[1][0], 
        combinations(practical_seminar_groups, 2)
    )

    for u, v in seminar_combinations:
        course_u = courses[u[0]]
        course_v = courses[v[0]]

        # check if schedules of practical seminars overlap
        group_u = course_u.practical_seminars[u[1]]
        group_v = course_v.practical_seminars[v[1]]
        seminars_overlap = group_u.overlaps(group_v)

        # check if schedule of group overlaps with any lecture or misc event of the
        # course the other group belongs to
        course_v_overlap = course_v.lectures.overlaps(group_u) or course_v.misc.overlaps(group_u)
        course_u_overlap = course_u.lectures.overlaps(group_v) or course_u.misc.overlaps(group_v)
        
        # only add edge if there is no overlap
        if not (seminars_overlap or course_v_overlap or course_u_overlap):
            G.add_edge(u, v)
    
    # find cliques
    number_of_courses = len(courses)
    cliques = filter(lambda x: len(x) == number_of_courses, nx.find_cliques(G))
    cliques = map(sorted, cliques)

    # create df and rename columns
    df = pd.DataFrame(data=cliques)
    column_names = list(map(lambda x: x[0], df.loc[0,:].values))
    df.set_axis(column_names, axis=1, inplace=True)
    df.sort_values(column_names, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df
