import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import defaultdict

overcount = {1: 2, 2: 3, 4: 3, 3: 2, 6: 1, 5: 4, 7: 2, 8: 4, 11: 4, 10: 2, 14: 2, 9: 2, 12: 2, 16: 1, 17: 1, 13: 1, 19: 1, 23: 1, 20: 3, 22: 3, 18: 4, 15: 5, 21: 1, 24: 2, 25: 1, 26: 1, 27: 4, 28: 2, 29: 5, 0: 2}
cols_toExtract = [0, 1, 3, 4, 6, 8, 9, 12, 14, 15, 18, 22, 24, 27, 31, 34, 35, 39, 43, 45, 49, 51, 54, 56, 59, 62, 65, 68, 70, 72]
#k=3: 2, k=4: 6, k=5: 21 
kcols = [(0,3), (3, 9), (9,30)]
def orca_to_lower(orbit,mapping):
        x = mapping[:,7]
        rows = np.where(x == orbit)
        
        return mapping[rows[0], 4]

def get_freq(orcaData):
    histogram = defaultdict(float)
    for node in range(orcaData.shape[0]):
        for orbit, col in enumerate(cols_toExtract):
            orbitCount = int(orcaData[node,col])
            histogram[orbit] += orbitCount
  
    for kcol in kcols:
        
        for orbit in range(kcol[0],kcol[1]):
            histogram[orbit] /= overcount[orbit]
        total = 0
        for orbit in range(kcol[0],kcol[1]):
            total += histogram[orbit]
        for orbit in range(kcol[0],kcol[1]):
            histogram[orbit] /= total
    
    print(sum(val for val in histogram.values()))
    assert(round(sum(val for val in histogram.values())) == 3 )
    return histogram    
        
def graph_freq(orcaDataFiles, orbitMap, k):
    ordinalPlots = []
    ordinalCounts = [[i] for i in range(len(cols_toExtract))]
    plt.yscale('log')
    for orcaDataFile in orcaDataFiles:
        orcaData = np.loadtxt(orcaDataFile)
        ordinalFreq = get_freq(orcaData)
        ordinalPlot, = plt.plot(ordinalFreq.keys(), ordinalFreq.values())
        print(ordinalFreq)
        for k in range(len(cols_toExtract)):
            ordinalCounts[k].append(ordinalFreq[k])
        ordinalPlots.append(ordinalPlot)

    toWrite = open("squiggly_plot.txt", 'w')
    toWrite.write("\t".join(['#'] + orcaDataFiles) + "\n")
    for line in ordinalCounts:
        toWrite.write("\t".join(str(w) for w in line) + "\n")
    toWrite.close()
    plt.xticks(range(len(cols_toExtract)), [orbit for orbit in range(len(cols_toExtract))], fontsize=7)
    plt.legend(ordinalPlots, orcaDataFiles)
    plt.xlabel("(ORCA graphlet (0 - 29))")

    plt.tight_layout()
    plt.savefig("squiggly_plot_k_" + str(k) + ".png")
    

def genOrbitToOrdinalMap(k):
    orbitToOrdinal = [-1 for i in range(len(cols_toExtract))]
    for ki in range(3,int(k)+1):
        mapping = np.loadtxt("orca_jesse_blant_table/UpperToLower"+str(ki)+".txt")
        for orbit in range(len(cols_toExtract)):
            if orbitToOrdinal[orbit] < 0:
                ordinal_loc = orca_to_lower(orbit, mapping)
                if len(ordinal_loc) > 0:
                    orbitToOrdinal[orbit] = ordinal_loc[0]
    return orbitToOrdinal
    




if __name__ == '__main__':
    orcaDataFiles = sys.argv[1:-1]
    k = sys.argv[-1]
    orbitMap = genOrbitToOrdinalMap(k)
    graph_freq(orcaDataFiles, orbitMap, k)
    
    
    