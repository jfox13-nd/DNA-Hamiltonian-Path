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
    "0": "1",   # A
    "1": "0",   # T
    "2": "3",   # C
    "3": "2"    # G
}

def usage():
    print("""
usage: {} graph.json start_vertex end_vertex
    """.format(sys.argv[0]))
    sys.exit(0)

def get_all_vertex(graph: dict, vertex_mapping: dict) -> None:
    """ Generate a string encoding for each vertex and record each recording in the vertex_mapping dict """
    for vertex in graph:
        generate_vertex_encoding(vertex, vertex_mapping)

def generate_vertex_encoding(vertex: str, vertex_mapping: dict) -> None:
    """ Generate a string encoding of a vertex that is representative of a DNA strand """
    encoding = generate_random_string(20)
    while encoding[10:] in partial_vertex_encodings or encoding[:10] in partial_vertex_encodings:
        encoding = generate_random_string(20)
    partial_vertex_encodings.add(encoding[10:])
    partial_vertex_encodings.add(encoding[:10])
    vertex_encodings.add(encoding)
    vertex_mapping[vertex] = encoding

def generate_random_string(size: int) -> str:
    """ Generate a string of a given size consisting of characters 0,1,2, and 3 """
    return "".join([ str(random.randrange(4)) for _ in range(size) ])

def get_complement_encoding(s: str) -> str:
    """ Generate the Watson-Crick complement string encoding of a DNA strand string encoding """
    return "".join([ base_mapping[i] for i in s ])

def generate_edge(vertex_5: str, vertex_3: str) -> str:
    """ Generate the edge between two vertex DNA strands """
    return "".join([ get_complement_encoding(vertex_5[10:]), get_complement_encoding(vertex_3[:10]) ])

def generate_all_edges(graph: dict, edge_encodings: set) -> None:
    """ Generate string encoding representations of each edge in the directed graph, record this information in the edge_encodings set """
    for vertex in graph:
        for v in graph[vertex]:
            edge_encodings.add(generate_edge(vertex_mapping[vertex],vertex_mapping[v]))

def connected_edges(edge_a: str, edge_b: str) -> str:
    """ Determine if two edges can logically follow each other in a graph based on string encodings for those edges and the encodings of every vertex """
    vertex = get_complement_encoding("{}{}".format(edge_a[10:],edge_b[:10]))
    if vertex in vertex_encodings:
        return vertex
    return None

def is_valid_path(edge_list: list) -> list:
    """ Determine if a list of string encodings for edges is a valid path through the directed graph """
    path = []
    # add first vertex
    partial_vertex = get_complement_encoding(edge_list[0][:10])
    if partial_vertex not in partial_vertex_encodings:
        return None
    for vertex in vertex_encodings:
        if partial_vertex == vertex[10:]:
            path.append(vertex)
    # add middle vertices
    for i in range(len(edge_list)-1):
        vertex = connected_edges(edge_list[i],edge_list[i+1])
        if not vertex:
            return None
        path.append(vertex)
    # add last vertex
    partial_vertex = get_complement_encoding(edge_list[-1][10:])
    if partial_vertex not in partial_vertex_encodings:
        return None
    for vertex in vertex_encodings:
        if partial_vertex == vertex[:10]:
            path.append(vertex)
    return path

def generate_all_possible_solutions(edge_encodings: set, possible_solutions: list) -> None:
    """
    Generates many possible paths through the graph.
    Many more paths are generated than are required for a solution, this is done intentionally to mimic how this algorithm would be executed in a laboratory
    Every permutation of edge encodings is produced.
    Edges may be repeated and possible solutions of varying sizes are also produced.
    """
    edge_bank = []
    for edge in edge_encodings:
        edge_bank.append(edge)
        edge_bank.append(edge)
    
    min_size = 2
    max_size = len(edge_encodings) + 2
    for i in range(min_size, max_size):
        for perm in permutations(edge_bank, i):
            possible_solution = is_valid_path(perm)
            if possible_solution:
                possible_solutions.append(possible_solution)

def convert_edges_to_vertices(edge_list: list) -> list:
    """ Converts a list of edges into a list of vertices """
    vertices_list = []
    for i in range(len(edge_list)-1):
        vertices_list.append( get_complement_encoding("{}{}".format(edge_list[i][10:],edge_list[i+1][:10])))
    return vertices_list

def eliminate_invalid_endings(possible_solutions: list, start_vertex: str, end_vertex: str) -> None:
    """ Eliminates strands from the possible_solutions list that don't start and end at the provided vertices """
    solutions_to_remove = []
    for solution in possible_solutions:
        if solution[0] != start_vertex or solution[-1] != end_vertex:
            solutions_to_remove.append(solution)
    for bad_solution in solutions_to_remove:
        possible_solutions.remove(bad_solution)

def eliminate_wrong_size(possible_solutions: list, vertex_encodings: set)-> None:
    """ Eliminates strands that do not have the correct number of vertices """
    solutions_to_remove = []
    for solution in possible_solutions:
        if not len(solution) == len(vertex_encodings):
            solutions_to_remove.append(solution)
    for bad_solution in solutions_to_remove:
        possible_solutions.remove(bad_solution)

def eliminate_missing_vertex(possible_solutions: list, vertex_encodings: set)-> None:
    """ Eliminates strands that are missing a vertex """
    solutions_to_remove = []
    for solution in possible_solutions:
        for vertex in vertex_encodings:
            if not vertex in solution:
                solutions_to_remove.append(solution)
                break
    for bad_solution in solutions_to_remove:
        possible_solutions.remove(bad_solution)

def vertex_list_human_readable(vertex_list: list) -> str:
    """ Return a human readable path from a strand of vertices """
    human_readable = ""
    for v in vertex_list:
        for vm in vertex_mapping:
            if vertex_mapping[vm] == v:
                human_readable = "{}{}".format(human_readable,vm)
    return human_readable


if __name__ == '__main__':
    if(len(sys.argv) != 4):
        usage()
    start_vertex = sys.argv[2].strip()
    end_vertex = sys.argv[3].strip()

    with open(sys.argv[1]) as json_file:
        graph = json.load(json_file)

    print("Creating DNA strands for vertices and edges")
    get_all_vertex(graph, vertex_mapping)
    generate_all_edges(graph, edge_encodings)

    print("The following are vertex encodings")
    for v in vertex_mapping:
        print("{}: 5' {} 3'".format(v,vertex_mapping[v]))

    print("Generating strands encompassing all possible solutions")
    generate_all_possible_solutions(edge_encodings, possible_solutions)

    print("Eliminating strands that don't start and end with the specified vertices")
    eliminate_invalid_endings(possible_solutions,vertex_mapping[start_vertex],vertex_mapping[end_vertex])
    if not possible_solutions:
        print("There are no remaining strands that could be possible solutions")

    print("Eliminating strands that are not the correct size")
    eliminate_wrong_size(possible_solutions, vertex_encodings)
    if not possible_solutions:
        print("There are no remaining strands that could be possible solutions")

    print("Eliminating strands that don't include every vertex")
    eliminate_missing_vertex(possible_solutions, vertex_encodings)

    hamil_paths = set()
    if possible_solutions:
        print("YES, this is a valid Hamiltonian path")
        print("Valid Solutions:")
        for soln in possible_solutions:
            hamil_paths.add(tuple(soln))
        for hamil in hamil_paths:
            print("".join(hamil))
            print(vertex_list_human_readable(hamil))
    else:
        print("NO, this is not a valid Hamiltonian path")