#!/usr/bin/env python3

import sys
import json
import random
from itertools import permutations

vertex_mapping = {}
partial_vertex_encodings = set()
vertex_encodings = set()
edge_encodings = set()
possible_solutions = []
graph = {}
base_mapping = {
    "0": "1",
    "1": "0",
    "2": "3",
    "3": "2"
}

def usage():
    print("""
usage: {} graph.json start_vertex end_vertex
    """.format(sys.argv[0]))
    sys.exit(0)

def get_all_vertex(graph: dict, vertex_mapping: dict) -> None:
    for vertex in graph:
        generate_vertex_encoding(vertex, vertex_mapping)

def generate_vertex_encoding(vertex: str, vertex_mapping: dict) -> None:
    encoding = generate_random_string(20)
    while encoding[10:] in partial_vertex_encodings or encoding[:10] in partial_vertex_encodings:
        encoding = generate_random_string(20)
    partial_vertex_encodings.add(encoding[10:])
    partial_vertex_encodings.add(encoding[:10])
    vertex_encodings.add(encoding)
    vertex_mapping[vertex] = encoding

def generate_random_string(size: int) -> str:
    return "".join([ str(random.randrange(4)) for _ in range(size) ])

def get_complement_encoding(s: str) -> str:
    return "".join([ base_mapping[i] for i in s ])

def generate_edge(vertex_5: str, vertex_3: str) -> str:
    return "".join([ get_complement_encoding(vertex_5[10:]), get_complement_encoding(vertex_3[:10]) ])

def generate_all_edges(graph: dict, edge_encodings: set) -> None:
    for vertex in graph:
        for v in graph[vertex]:
            edge_encodings.add(generate_edge(vertex_mapping[vertex],vertex_mapping[v]))

def connected_edges(edge_a: str, edge_b: str) -> str:
    vertex = get_complement_encoding("{}{}".format(edge_a[10:],edge_b[:10]))
    if vertex in vertex_encodings:
        return vertex
    return None
    #return get_complement_encoding("{}{}".format(edge_a[10:],edge_b[:10])) in vertex_encodings

def is_valid_path(edge_list: list) -> list:
    path = []
    for i in range(len(edge_list)-1):
        vertex = connected_edges(edge_list[i],edge_list[i+1])
        if not vertex:
            return None
        path.append(vertex)
    return path

def generate_all_possible_solutions(edge_encodings: set, possible_solutions: list) -> None:
    edge_bank = []
    for edge in edge_encodings:
        edge_bank.append(edge)
        edge_bank.append(edge)
    
    min_size = max(2, len(edge_encodings)-2)
    max_size = len(edge_encodings) + 2
    print(len(edge_encodings))
    for i in range(min_size, max_size):
        print(i)
        for perm in permutations(edge_bank, i):
            possible_solution = is_valid_path(perm)
            if possible_solution:
                possible_solutions.append(possible_solution)

            #if is_valid_path(perm):
            #    perm = convert_edges_to_vertices(perm)
            #    possible_solutions.append(perm)

def convert_edges_to_vertices(edge_list: list) -> list:
    vertices_list = []
    for i in range(len(edge_list)-1):
        vertices_list.append( get_complement_encoding("{}{}".format(edge_list[i][10:],edge_list[i+1][:10])))
    return vertices_list

'''
def eliminate_invalid_endings(possible_solutions: list, start_vertex: str, end_vertex: str) -> None:
    solutions_to_remove = []
    for solution in possible_solutions:
        if get_complement_encoding(solution[0][:10]) != start_vertex[10:] or get_complement_encoding(solution[-1][10:]) != end_vertex[:10]:
            solutions_to_remove.append(solution)
    for bad_solution in solutions_to_remove:
        possible_solutions.remove(bad_solution)
'''

def eliminate_invalid_endings(possible_solutions: list, start_vertex: str, end_vertex: str) -> None:
    solutions_to_remove = []
    for solution in possible_solutions:
        if solution[0] != start_vertex or solution[-1] != end_vertex:
            solutions_to_remove.append(solution)
    for bad_solution in solutions_to_remove:
        possible_solutions.remove(bad_solution)

def eliminate_wrong_size(possible_solutions: list, vertex_encodings: set)-> None:
    solutions_to_remove = []
    for solution in possible_solutions:
        if not len(solution) == len(vertex_encodings):
            solutions_to_remove.append(solution)
    for bad_solution in solutions_to_remove:
        possible_solutions.remove(bad_solution)

def eliminate_missing_vertex(possible_solutions: list, vertex_encodings: set)-> None:
    solutions_to_remove = []
    for solution in possible_solutions:
        for vertex in vertex_encodings:
            if not vertex in solution:
                solutions_to_remove.append(solution)
                break
    for bad_solution in solutions_to_remove:
        possible_solutions.remove(bad_solution)


if __name__ == '__main__':
    if(len(sys.argv) != 4):
        usage()
    start_vertex = sys.argv[2].strip()
    end_vertex = sys.argv[3].strip()

    with open(sys.argv[1]) as json_file:
        graph = json.load(json_file)

    get_all_vertex(graph, vertex_mapping)
    generate_all_edges(graph, edge_encodings)
    generate_all_possible_solutions(edge_encodings, possible_solutions)

    if possible_solutions:
        print("YES")
    else:
        print("NO")

    #print(possible_solutions)
    '''
    for s in possible_solutions:
        for v in s:
            if v == vertex_mapping[start_vertex]:
                print("HELLO")
    '''

    eliminate_invalid_endings(possible_solutions,vertex_mapping[start_vertex],vertex_mapping[end_vertex])
    if possible_solutions:
        print("YES")
    else:
        print("NO")
    eliminate_wrong_size(possible_solutions, vertex_encodings)
    if possible_solutions:
        print("YES")
    else:
        print("NO")
    eliminate_missing_vertex(possible_solutions, vertex_encodings)

    if possible_solutions:
        print("YES, this is a valid Hamiltonian path")
    else:
        print("NO, this is not a valid Hamiltonian path")