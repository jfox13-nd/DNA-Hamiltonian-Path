# DNA-Hamiltonian-Path
A simulator of Adleman's Hamiltonian path algorithm, written in Python.

## Usage
```
Usage: algorithm.py graph.json start_vertex end_vertex
```
The algorithm will attempt to find a Hamiltonian path between vertex `start_vertex` and vertex `end_vertex`.
Describe your directed graph in a file `graph.json` in the following format:
```
{
    "A": ["B","C"],
    "B": ["C","D"],
    "C": ["B","D"],
    "D": []
}
```
Where:
```
    "A": ["B","C"],
```
Would indicate an edge from vertex "A" to vertex "B" and another edge from vertex "A" to vertex "B"

## Sample Inputs
The included `graph.json` includes a simple graph that has multiple Hamiltonian paths between vertices "A" and "D":
`$ python3 algorithm.py graph.json A D`