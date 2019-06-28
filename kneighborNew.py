from numpy.linalg import matrix_power
from matplotlib import pyplot as plt
from collections import defaultdict
import sys
from math import inf
from copy import copy
def elToGraph(efile):
    graph = defaultdict(set) 
    def toInf():
        return inf
    dist = defaultdict(toInf)
    for line in open(efile, 'r'):
        node1, node2 = line.split()
        if node2 != node1:
            graph[node1].add(node2)
            graph[node2].add(node1)
            dist[(node1,node2)] = 1
            dist[(node2,node1)] = 1
    print(len(graph))
    #print((sum(len(v) for v in k,v in graph.items()))/ len(graph))
    return graph, dist
            
def getKclosure(graph, k):
    indexToNode = [node for node in graph]
    mat = [[1 if indexToNode[i] in graph[indexToNode[j]] else 0 for i in range(len(indexToNode))] for j in range(len(indexToNode))]
    mat = matrix_power(mat, max(1,k-2))
    ret = set()
    for i in range(len(indexToNode)):
        for j in range(i):
            if mat[i][j] > 0:
                ret.add((indexToNode[i],indexToNode[j]))
    
    return ret

def getCkFloydWarshall(graph, nodes, node, kval, srcDist):
    C_k = [0 for i in range(max(kval - 2, 0))]
    dist = copy(srcDist)
    neighbors = [v for v in graph[node]]
    for k in filter(lambda x: x != node, nodes):
        for lim, i in enumerate(filter(lambda x: x != node and x != k, nodes)):
            for j in filter(lambda x: x!= node and x != k and x != i, nodes):
                if dist[(i,k)] + dist[(k,j)] < dist[(i,j)]:
                    dist[(i,j)] =  dist[(i,k)] + dist[(k,j)]
    for pos,i in enumerate(neighbors):
        for j in neighbors[:pos]:
            path = dist[(i,j)]
            if path != inf:    
                for index in range(path, len(C_k)):
                    C_k[index] += 1
    n = len(graph[node])
    allPairCount = max(((n * (n-1)) // 2 ), 1)
    return [kCount /  allPairCount for kCount in C_k]


if __name__ == '__main__':
    files = sys.argv[1:-1]
    k = int(sys.argv[-1])
    C_kVals_arr = []
    for el in files:
        graph,dist = elToGraph(el)
        #pairs = getKclosure(graph, k)
        C_kVals = defaultdict(int)
        for node in graph.keys():
            for pathIndex, coefficient in enumerate(getCkFloydWarshall(graph, [key for key in graph.keys()], node, k, dist)):
                C_kVals[pathIndex + 1] += coefficient
        for key in C_kVals.keys():
            C_kVals[key] /= len(graph)
        print(C_kVals)
        C_kVals_arr.append(C_kVals)

    for C_kVals in C_kVals_arr:
        plt.plot([i for i in range(3, k+1)], [C_kVals[i] for i in range(1,k-1)])
    plt.xlabel('K values (Note that paths for a given k are from 1 to k-2)')
    plt.ylabel('Cycle coefficients')
    plt.savefig('-'.join(files) + "_k_" + str(k) + ".png")