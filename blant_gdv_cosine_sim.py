import graphlet
import numpy as np
from scipy import spatial
from sys import argv
import matplotlib.pyplot as plt
from os import path

def graphlet_setup(k):
    graphlet.K = k
    print(graphlet.K)
    graphlet.set_canon_list()
    graphlet.set_upperToLower()

def build_gdv_comparisons(gdvs, graphlets):
    print(len(gdvs))
    gdv_comparisons = np.zeros((len(gdvs), len(gdvs)))
    for i,gdv1 in enumerate(gdvs):
        for j, gdv2 in enumerate(gdvs):
            gdv_comparisons[i,j] = gdv_comparisons[j,i] if j < i else 1 - spatial.distance.cosine(gdv1, gdv2) 
    return gdv_comparisons

def blant_compute_gdv_sim(gfiles, k):
    graphlet_setup(k)
    gdv0 = np.loadtxt(gfiles[0])
    graphlets = [graphlet.Graphlet(lower_ord=line) for line in gdv0[:,1]]
    gdv0 = gdv0[:,0]
    gdvs = [gdv0] + [np.loadtxt(gfil)[:,0] for gfil in gfiles[1:]]
    gdv_cos_table = build_gdv_comparisons(gdvs, graphlets)
    return gdv_cos_table

def draw_table(matrix, labels):
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=matrix, colLabels=labels, rowLabels=labels, loc='center', fontsize='70')
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    gfiles, k = argv[1:-1], int(argv[-1])
    draw_table(blant_compute_gdv_sim(gfiles,k), [path.split(fil)[-1] for fil in gfiles])
