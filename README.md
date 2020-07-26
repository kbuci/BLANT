# BLANT fork
# Graphlet plotting tools "Squiggly Plots"

The included python3 scripts are used for generating graphlet concentration plots from BLANT -mf output

Required are python3 and the python packages `numpy` and `matplotlib`

To get the top X largest concentrations of graphlets from one or more files

`python3 graphletTopKPlot.py blant_output_1 blant_output_2 ... blant_output_n k X`

For the other scripts, note that "Trees" are graphlets where every two nodes is connected by exactly one path, and "Stars" are
k-graphlets where one node has degree k-1.

To plot all the graphlet concentrations from one or more files that correspond to "Stars", "Trees" or cliques

`python3 graphletConcPlot.py blant_output_1 blant_output_2 ... blant_output_n k`

To generate images of the graphlets for the concentrations use the alternate script:

`python3 graphletConcPlotImg.py blant_output_1 blant_output_2 ... blant_output_n k`

Note that this latter script requires every "Tree"/"Star"/clique graphlet for the given k to be included as a image in /Draw/GraphletImages
as \[lower_ordinal of graphlet\]img.png
