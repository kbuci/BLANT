from graphlet import Graphlet
import graphlet
import numpy as np
from matplotlib.offsetbox import (DrawingArea, OffsetImage,AnnotationBbox)
import matplotlib.pyplot as plt
from matplotlib.image import BboxImage, imread
from matplotlib.transforms import Bbox
import matplotlib.patches as patches
import sys
from PIL import Image, ImageChops
from os import path

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def implot(ax, lowers):
  
    ax.get_xaxis().set_ticks(range(len(lowers)))
    ax.get_xaxis().set_ticklabels(lowers)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    def get_abs_dist(percent):
        return percent * (xmax - xmin),  percent * (ymax - ymin) 
        
    print(ax.get_ylim())
    print(ax.get_xlim())
    for idx, lower in enumerate(lowers):
        xdist, ydist = get_abs_dist(.15)

        lowerCorner = ax.transAxes.transform((idx/len(lowers),0))
        upperCorner = ax.transAxes.transform(((idx+1)/len(lowers), .1))
        print(lowerCorner, upperCorner)
        #lowerCorner, upperCorner = (idx - .5,ymin),(idx + .5, ydist + ymin)
        bbox_image = BboxImage(Bbox([[lowerCorner[0],
                             lowerCorner[1]],
                             [upperCorner[0],
                             upperCorner[1]]]),
                       norm = None,
                       origin=None,
                       clip_on=False)
        img_arr = Image.open('Draw/'+str(lower)+'img.png')
        img = trim(img_arr)
        img.thumbnail((265,256), Image.ANTIALIAS)
        
        bbox_image.set_data(img)
        ax.add_artist(bbox_image)
        
        prect = patches.Rectangle((idx-.5,ymin),1,ydist,color="Red" if idx % 2 == 0 else "Blue",
                               fill=False,clip_on=False)
        #ax.add_patch(prect)
    


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

    fig = plt.figure(figsize=(30,10))
    ax = fig.add_subplot(111)

    

    graphlet.K = k
    print(graphlet.K)
    graphlet.set_canon_list()
    graphlet.set_upperToLower()
    plots = []
    #plt.yscale('log')
    concFile = concFiles[0]
    concData = np.loadtxt(concFile, dtype={'names':('conc','lower'),'formats':('float','int')})
    graphlets = [Graphlet(lower_ord=line[1]) for line in concData]
    topGraphletRows = set()
    graphletRows = [i for i in range(len(graphlets))]
    for concFile in concFiles: 
        concData = np.loadtxt(concFile, dtype={'names':('conc','lower'),'formats':('float','int')})
        topGraphletRows = topGraphletRows.union(set(sorted(graphletRows, reverse=True, key=lambda row: concData[row][0])[:5]))
    
    print(topGraphletRows)
    topGraphletRows = sorted(list(topGraphletRows),key = lambda row: graphlets[row].lower_decimal)
    graphlets = [graphlets[row] for row in topGraphletRows]
    
    for concFile in concFiles:
        concData = np.loadtxt(concFile, dtype={'names':('conc','lower'),'formats':('float','int')})
        concPlot, = ax.plot([concData[row][0] for row in topGraphletRows])
        plots.append(concPlot)
    

    #implot(ax, [graphlets[row].lower_decimal for row in rows])
    plt.yscale('log')
    plt.xlabel("(BLANT lower decimal, Edge density)")
    plt.ylabel("Graphlet concentration")
    #plt.tight_layout()
    plt.tick_params(labelsize=20)
    ax.xaxis.label.set_fontsize(20)
    ax.yaxis.label.set_fontsize(20)
    
    #plt.rc('ytick', labelsize=30)
    plt.xticks(range(len(graphlets)), [(graphlet.lower_decimal,round(graphlet.getDensity(),3)) for graphlet in graphlets])
    fig.suptitle("BLANT sampling MCMC top 5 concentrations for each graph ", fontsize=30)
    plt.legend(plots, [path.split(fil)[-1] for fil in concFiles], bbox_to_anchor=(1,1), loc = 1, prop={'size':20})    
    plt.savefig("squiggly_plot_conc_k" + str(k) + "_top_values_union.png")
    
    



if __name__ == '__main__':
    plotConcFiles(sys.argv[1:-1],int(sys.argv[-1]))




