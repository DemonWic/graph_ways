from sys import argv
import networkx as nx
from copy import deepcopy


def delete_way(buf: dict, edges: set, lst: list):
    lst = lst[1:-1]
    for i in lst:
        if i in buf.keys():
            buf.pop(i)
    edges2 = deepcopy(edges)
    for i in edges:
        if i[0] in lst or i[1] in lst:
            edges2.remove(i)
    return buf, edges2


def get_way(nodes: dict, edges: set, start: str, end: str):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(edges)
    buf = nx.dijkstra_path(graph, start, end)
    return buf


def get_ways(nodes: dict, edges: set, start: str, end: str):
    res = []
    i = 0
    while i < 100:
        try:
            buf = get_way(nodes, edges, start, end)
            res.append(buf)
            nodes, edges = delete_way(nodes, edges, buf)
        except Exception as e:
            return res
        i += 1
    return res


if __name__ == '__main__':
    if len(argv) > 1:
        file_name = argv[1]
    else:
        print("Файл с графом не указан")
        exit(0)
    buf = {}
    edges = set()
    k = 0
    with open(file_name, 'r') as f:
        global start
        global end
        for line in f:
            line = line.strip()
            if "##start" == line:
                k = 1
            elif "##end" == line:
                k = 2
            elif "#" in line:
                continue
            elif " " in line:
                line = line.split()
                buf[line[0]] = [int(line[1]), int(line[2])]
                if k == 1:
                    start = line[0]
                    k = 0
                elif k == 2:
                    end = line[0]
                    k = 0
            elif "-" in line:
                line = line.split('-')
                edges.add((line[0], line[1], 1))

    res = get_ways(buf, edges, start, end)
    for i in res:
        print(str(i) + str(len(i)))
        print("\n")