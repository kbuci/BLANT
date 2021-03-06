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
        img_arr = Image.open('Draw/GraphletImages/'+str(lower)+'img.png')
        img = trim(img_arr)
        img.thumbnail((265,256), Image.ANTIALIAS)
        
        bbox_image.set_data(img)
        ax.add_artist(bbox_image)    


def plotConcFiles(concFiles, k):
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
    rows = list(filter(lambda i: graphlets[i].isTree() or graphlets[i].isStar() or graphlets[i].isClique(),range(len(graphlets))))
    

    for concFile in concFiles: 
        concData = np.loadtxt(concFile, dtype={'names':('conc','lower'),'formats':('float','int')})
        concPlot, = ax.plot([concData[row][0] for row in rows])
        plots.append(concPlot)

    implot(ax, [graphlets[row].lower_decimal for row in rows])
    plt.yscale('log')
    plt.xlabel("BLANT lower decimal")
    plt.ylabel("Graphlet concentration")
    #plt.tight_layout()
    plt.tick_params(labelsize=30)
    ax.xaxis.label.set_fontsize(20)
    ax.yaxis.label.set_fontsize(20)
    
    #plt.rc('ytick', labelsize=30)
    fig.suptitle("BLANT sampling MCMC concentrations of graphlet stars, trees, and cliques", fontsize=30)
    plt.legend(plots, [path.split(fil)[-1] for fil in concFiles], bbox_to_anchor=(1,1), loc = 1, prop={'size':20})
    
    plt.savefig("squiggly_plot_conc_k" + str(k) + ".png")
    
    



if __name__ == '__main__':
    plotConcFiles(sys.argv[1:-1],int(sys.argv[-1]))




