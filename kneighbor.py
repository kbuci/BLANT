

from numpy.linalg import matrix_power
from matplotlib import pyplot as plt
from collections import defaultdict
import sys

def elToGraph(efile):
    graph = defaultdict(set) 
    for line in open(efile, 'r'):
        node1, node2 = line.split()
        if node2 != node1:
            graph[node1].add(node2)
            graph[node2].add(node1)
    print(len(graph))
    #print((sum(len(v) for v in k,v in graph.items()))/ len(graph))
    return graph
            
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

#b*k
def isKConnected(graph, node, u, v, k):
    frontier = [u]
    explored = set()
    for i in range(max(0,k-2)):
        if len(frontier) == 0:
           return -1
        newFrontier = []
        for parent in frontier:
            for child in graph[parent]:
                if child != node and child not in explored:
                    newFrontier.append(child)
                    explored.add(child)
                elif child == v:
                    return i
        frontier = [n for n in newFrontier]
    return -1


#V * ( nCr(d, 2) * ((d^k-2) + k-2)))
#V * ( k * d^2 + d^k ) vs V * (V * (E/V)**2))
def getCk(graph, node, k):
    C_k = [0 for i in range(max(k - 2, 0))]
    neighbors = [n for n in graph[node]]
    for index, u in enumerate(neighbors):
        for v in neighbors[:index]:
            kDist = isKConnected(graph, node, u,v,k)
            if kDist >= 1:
                for i in range(kDist, max(k - 2, 0)):
                    C_k[i] += 1
    n = len(graph[node])
    allPairCount = max(((n * (n-1)) // 2 ), 1)
    return [kCount / allPairCount for kCount in C_k]

if __name__ == '__main__':
    files = sys.argv[1:-1]
    k = int(sys.argv[-1])
    C_kVals_arr = []
    for el in files:
        graph = elToGraph(el)
        C_kVals = defaultdict(int)
        for node in graph.keys():
            for pathIndex, coefficient in enumerate(getCk(graph, node, k)):
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