from graphletConcPlotImg import implot
from graphlet import Graphlet
import graphlet
import matplotlib.pyplot as plt
import numpy as np
import sys
from os import path, listdir, sep

def getSampleSize(concFolder):
    return len(listdir(concFolder))
def getFirstSample(concFolder):
    concFile = path.join(concFolder, listdir(concFolder)[0])
    return concFile

def collectGraphletSamples(concFolder, sampleGraphlets):
    numSamples = getSampleSize(concFolder)
    sampleSize = len(sampleGraphlets)
    sampleData = np.zeros((sampleSize, numSamples))
    for sampleNo, sampleFil in enumerate(listdir(concFolder)):
        fil = path.join(concFolder,sampleFil)
        concData = np.loadtxt(fil, dtype={'names':('conc','lower'),'formats':('float','int')})
        sampleData[:,sampleNo] = [concData[g][0] for g in sampleGraphlets]
        #print(sampleData[sampleNo,:])
    return sampleData

def plotConcFolder(concFolder, k):
    def writeShape(g):
        ret = str(g.lower_decimal)
        if g.isStar():
            return ret + "*"
        if g.isTree():
            return ret + "T"
        if g.isClique():
            return ret + "C"
        return ret

    fig = plt.figure(figsize=(30,10))
    ax = fig.add_subplot(111)

    

    graphlet.K = k
    print(graphlet.K)
    graphlet.set_canon_list()
    graphlet.set_upperToLower()
    #plt.yscale('log')
    concFile = getFirstSample(concFolder)
    concData = np.loadtxt(concFile, dtype={'names':('conc','lower'),'formats':('float','int')})
    graphlets = [Graphlet(lower_ord=line[1]) for line in concData]
    selected_graphlets = list(filter(lambda i: graphlets[i].isTree() or graphlets[i].isStar() or graphlets[i].isClique(),range(len(graphlets))))
    
    sampleData = collectGraphletSamples(concFolder, selected_graphlets)
    print(sampleData.shape)
    #ax.boxplot([sampleData[:,i] for i,s in enumerate(selected_graphlets) ])
    ax.boxplot(sampleData.tolist())
    implot(ax, [graphlets[row].lower_decimal for row in selected_graphlets])
   
    plt.xlabel("BLANT lower decimal")
    plt.ylabel("Graphlet concentration")
    concPath = path.normpath(concFolder)
    dirLabel = concPath.split(sep)[-1]
    print(dirLabel)
    plt.tick_params(labelsize=30)
    ax.xaxis.label.set_fontsize(20)
    ax.yaxis.label.set_fontsize(20)
    plt.title(dirLabel + " k=" + str(k))
    
    #plt.tight_layout
    #plt.legend(plots, [path.split(fil)[-1] for fil in concFiles], bbox_to_anchor=(1,1), loc = 1, prop={'size':20})
    plt.savefig("squiggly_plot_conc_dist_k" + str(k) + "_" + dirLabel + ".png")
    
    



if __name__ == '__main__':
    plotConcFolder(sys.argv[1],int(sys.argv[-1]))




