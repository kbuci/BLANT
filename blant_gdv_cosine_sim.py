import graphlet
import numpy as np
from scipy import spatial
from sys import argv

def graphlet_setup(k):
    graphlet.K = k
    print(graphlet.K)
    graphlet.set_canon_list()
    graphlet.set_upperToLower()

def build_gdv_comparisons(gdvs, graphlets):
    gdv_comparisons = np.zeros(len(gdvs), len(gdvs))
    for i,gdv1 in enumerate(gdvs):
        for j, gdv2 in enumerate(gdvs):
            if j <= i:
                next()
            gdv_comparisons[i,j] = 1 - spatial.distance.cosine(gdv1, gdv2)
    return gdv_comparisons

def blant_compute_gdv_sim(gfiles, k):
    graphlet_setup(k)
    gdv0 = np.loadtxt(gfiles[0])
    graphlets = [graphlet.Graphlet(lower_ord=line[1]) for line in gdv0]
    gdv0 = gdv0[:,1]
    gdvs = [gdv0] + [np.loadtxt(gfil)[:,1] for gfil in gfiles[1:]]
    gdv_cos_table = build_gdv_comparisons(gdvs, graphlets)
    print(gdv_cos_table)


if __name__ == '__main__':
    gfiles, k = argv[1:-1], argv[-1]
    blant_compute_gdv_sim(gfiles,k)
