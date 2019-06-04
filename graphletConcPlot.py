from graphlet import Graphlet
import graphlet
import numpy as np
import matplotlib.pyplot as plt
import sys



def plotConcFiles(concFiles, k):
    def writeShape(g):
        ret = str(g.lower_decimal)
        if g.isStar():
            return ret + "*"
        if g.isTree():
            return ret + "T"
        if g.isClique():
            return ret + "C"
        return ret

    graphlet.K = k
    print(graphlet.K)
    graphlet.set_canon_list()
    graphlet.set_upperToLower()
    plots = []
    plt.yscale('log')
    concFile = concFiles[0]
    concData = np.loadtxt(concFile, dtype={'names':('conc','lower'),'formats':('float','int')})
    print(concData)
    graphlets = [Graphlet(lower_ord=line[1]) for line in concData]
    rows = list(filter(lambda i: graphlets[i].isTree() or graphlets[i].isStar() or graphlets[i].isClique(),range(len(graphlets))))

    for concFile in concFiles: 
        concData = np.loadtxt(concFile, dtype={'names':('conc','lower'),'formats':('float','int')})
        print(rows)
        concPlot, = plt.plot(range(len(rows)), [concData[row][0] for row in rows])
        plots.append(concPlot)

    print(rows)
    print([graphlets[row].lower_decimal for row in rows])
    plt.xticks(range(len(rows)), [writeShape(graphlets[row]) for row in rows])
    plt.legend(plots, concFiles)
    plt.xlabel("BLANT lower decimal, visual shape")
    plt.tight_layout()
    plt.savefig("squiggly_plot_conc.png")



if __name__ == '__main__':
    plotConcFiles(sys.argv[1:-1],int(sys.argv[-1]))




