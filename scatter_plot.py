"""
Usage: python scatter_plot.py <filename of log>
returns a .png file of the log in the location <ENTITY>/<logfilename>.png
Piture shows the location of entities, separated by the action

set ENTITY to tell for which entity do you want results
    usually CAO, CACL or SASM
"""

import sys
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np


def main(filename, ENTITY='SASM'):
    # Create dictionaries to save location
    # Key of dictionary is type of action, value is array of coordinates
    xloc = defaultdict(list)
    yloc = defaultdict(list)

    with open(filename, 'r') as f:
        for line in f:
            # Discard MoE events
            if "MoE:" in line:
                continue

            # Find entity
            entity, line = line.split(" => ")
            for i in range(len(entity)):
                if entity[i] == "#": # Iterate until #
                    entity = entity[:i] # discard number and #
                    break
            
            # If the entity name is "both", we rename CACL to CAO. Then we only count CAO, counting both
            if entity == "CACL" and ENTITY == "both":
                entity = "CAO"
            
            # If this is not the correct entity, check next line
            if entity != ENTITY: 
                continue

            # Split to keywords
            line = line.split()
            keyword = line[1]

            # find the location field, read coordinates
            for i in range(len(line)):
                if line[i] == "location:":
                    x_coordinate = float(line[i+1])
                    y_coordinate = float(line[i+2])
                    break
            
            # For one data anomaly, delete 0 coordinates 
            if x_coordinate == 0 and y_coordinate == 0:
                continue

            # Save x and y coordinates in the dictionary
            xloc[keyword].append(x_coordinate)
            yloc[keyword].append(y_coordinate)


    # Matplotlib 

    # So we count CAO, if ENTITY is "both". Because we transformed CACL entities to CAO, 
    # we now have to display CAO
    # name is for the save location & which name to display on the graph
    if ENTITY == "both":
        ENTITY = "CAO"
        name = "both"
    else:
        name = ENTITY

    
    fig, ax = plt.subplots()
    axis_len = 0
    for key in xloc:
        # Plot every action with a different colour
        plt.scatter(xloc[key], yloc[key], label=key)
    
    # Metadata about the graph
    ax.set_title('log: '+filename+'; entity: '+ name)
    ax.legend()
    fig.tight_layout()
    fig.set_size_inches(16, 12) # Size of the graph

    #plt.show() # Comment out for saving only
    plt.savefig(name+'/'+filename[:-4]+'.png', dpi=(100)) # Comment out for display only

    plt.close()
    return 0

# If no caller function
if __name__ == "__main__":
    main(sys.argv[1])
