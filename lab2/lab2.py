# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    new_agenda = []
    if start == []:
        return []
    elif start == goal:
        return [goal]
    if not isinstance(start, list):
        for node in graph.get_connected_nodes(start):
            new_path = [start, node]
            if node == goal:
                return new_path
            else:
                new_agenda.append(new_path)
    else:
        for path in start:
            for node in graph.get_connected_nodes(path[-1]):
                if node not in path:
                    new_path = path + [node]
                    if node == goal:
                        return new_path
                    else:
                        new_agenda.append(new_path)
    return bfs(graph, new_agenda, goal)
                
    

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    if start == []:
        return []
    elif start == goal:
        return [goal]
    if not isinstance(start, list):
        new_agenda = []
        for node in graph.get_connected_nodes(start):
            new_path = [start, node]
            if node == goal:
                return new_path
            else:
                new_agenda.append(new_path)
    else:
        path = start[0]
        if graph.get_connected_nodes(path[-1]) == []:
                return dfs(graph, start[1:], goal)
        else:
            new_agenda = start[1:]
            for next_node in graph.get_connected_nodes(path[-1]):
                new_path = path + next_node
                if next_node == goal:
                    return new_path
                new_agenda.insert(0, new_path)
    return bfs(graph, new_agenda, goal)


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    if start == []:
        return []
    elif start == goal:
        return [goal]
    if not isinstance(start, list):
        new_agenda = []
        options = sorted(graph.get_connected_nodes(start), key= lambda next_n: graph.get_heuristic(next_n, goal))
        for node in options:
            new_path = [start, node]
            if node == goal:
                return new_path
            else:
                new_agenda.append(new_path)
    else:
        path = start[0]
        new_agenda = start[1:]
        options = list(reversed(sorted(graph.get_connected_nodes(path[-1]), key= lambda next_n: graph.get_heuristic(next_n, goal))))
        for next_node in options:
            if next_node not in path:
                new_path = path + [next_node]
                if next_node == goal:
                    return new_path
                new_agenda.insert(0, new_path)
    return hill_climbing(graph, new_agenda, goal)

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    new_agenda = []
    possible_agenda = []
    if start == []:
        return []
    elif start == goal:
        return [goal]
    if not isinstance(start, list):
        for node in graph.get_connected_nodes(start):
            new_path = [start, node]
            if node == goal:
                return new_path
            else:
                possible_agenda.append(new_path)
    else:
        for path in start:
            for node in graph.get_connected_nodes(path[-1]):
                if node not in path:
                    new_path = path + [node]
                    if node == goal:
                        return new_path
                    else:
                        possible_agenda.append(new_path)
    if len(possible_agenda) < beam_width:
        return beam_search(graph, possible_agenda, goal, beam_width)
    else:
        new_agenda = sorted(possible_agenda, key= lambda path: graph.get_heuristic(path[-1], goal))[:beam_width]
        return beam_search(graph, new_agenda, goal, beam_width)
    

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    if len(node_names) == 0 or len(node_names) == 1:
        return 0
    else:
        length = 0
        actual_node = node_names[0]
        for next_node in node_names[1:]:
            length = length + graph.get_edge(actual_node, next_node).length
            actual_node = next_node
        return length
            


def branch_and_bound(graph, start, goal):
    if start == []:
        return []
    elif start == goal:
        return [goal]
    if not isinstance(start, list):
        possible_agenda = []
        for node in graph.get_connected_nodes(start):
            new_path = [start, node]
            if node == goal:
                return new_path
            else:
                possible_agenda.append(new_path)
    else:
        path = start[0]
        possible_agenda = start[1:]
        options = graph.get_connected_nodes(path[-1])
        for next_node in options:
            if next_node not in path:
                new_path = path + [next_node]
                if next_node == goal:
                    return new_path
                possible_agenda.append(new_path)
    new_agenda = sorted(possible_agenda, key= lambda path: path_length(graph, path))
    return branch_and_bound(graph, new_agenda, goal)

def a_star(graph, start, goal):
    return a_star_aux(graph, start, goal, {})
def a_star_aux(graph, start, goal, extended_set):
    ex_set = extended_set
    if start == []:
        return []
    elif start == goal:
        return [goal]
    if not isinstance(start, list):
        possible_agenda = []
        for node in graph.get_connected_nodes(start):
            new_path = [start, node]
            if node == goal:
                return new_path
            else:
                ex_set[node] = True
                possible_agenda.append(new_path)
    else:
        path = start[0]
        possible_agenda = start[1:]
        options = graph.get_connected_nodes(path[-1])
        for next_node in options:
            if next_node not in path and next_node not in ex_set:
                new_path = path + [next_node]
                if next_node == goal:
                    return new_path
                ex_set[next_node] = True
                possible_agenda.append(new_path)
    new_agenda = sorted(possible_agenda, key= lambda path: path_length(graph, path)+graph.get_heuristic(path[-1], goal))
    return a_star_aux(graph, new_agenda, goal, ex_set)


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?  heuristica(mapa) +

def is_admissible(graph, goal):
    for node in graph.nodes:
        path = a_star(graph, node, goal)
        if graph.get_heuristic(node, goal) > path_length(graph, path):
            return False
    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        tot = abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal))
        if edge.length < tot:
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '5'
WHAT_I_FOUND_INTERESTING = 'all'
WHAT_I_FOUND_BORING = 'nothing'
