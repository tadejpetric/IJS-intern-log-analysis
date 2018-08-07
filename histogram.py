"""
Usage: python histogram.py <filename of log>
returns a .png file of the log in the same directory as .log
Piture shows how often certain ActiveActions occur in a given
time interval

set TIME_INTERVAL to change the length (in seconds)
set DENSE_GRAPH to display x-axis as seconds, not intervals
    also makes the graph dense, without spaces between datapoints
set ENTITY to tell for which entity do you want results
    usually CAO, CACL or SASM
set MULTIPLOT to plot to True to graphs on different plots
    False overlays them
"""

import sys
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

def transfer(temporary, dd_timestamps, all_actions, timestamp):
    """
    Function for appending current intervals to the end result
    """
    for entity in temporary:
        for action in temporary[entity]:
            # We append the current interval to the end histogram plot
            # For every entity and action
            all_actions[entity][action].append(temporary[entity][action])
            # Also save timestamps because the data is not continuous
            # With this we keep track of the jumps. With this we save the
            # timestamp of the current interval
            dd_timestamps[entity][action].append(timestamp)
            temporary[entity][action] = 0 # Clear their data

def main(filename, weights,ENTITY='SASM', TIME_INTERVAL=5):
    temporary = defaultdict(lambda: defaultdict(int))
    all_actions = defaultdict(lambda: defaultdict(list))
    dd_timestamps = defaultdict(lambda: defaultdict(list))

    with open(filename, 'r') as f:
        timestamp = 0
        tempstamp = 0 # holds previous timestamp
        num_d = 0
        num_i = 0

        level_f = 0
        level_a = 0
        for line in f:
            # Discard MoE events, but count their instances
            if "MoE:" in line:
                if "Killed" in line:
                    num_d += 1 # global_killed also counts
                if "injured" in line:
                    num_i += 1
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

            # Split to keywords
            line = line.split()
            keyword = line[1]
            # find the action keyword and the timestamp
            for i in range(len(line)):
                if line[i] == "fear:":
                    level_f = float(line[i+1])
                elif line[i] == "anger:":
                    level_a = float(line[i+1])
                elif line[i] == "elapsedTime:" or line[i] == "timeElapsed:":
                    timestamp = int(float(line[i+1])) # Save the time
            
            # If we completed the interval, append the count to the end result
            # we check if 5 seconds has passed since the start of the last interval
            if timestamp >= tempstamp + TIME_INTERVAL:
                transfer(temporary, dd_timestamps, all_actions, tempstamp//TIME_INTERVAL)
                tempstamp = timestamp # Set the start time of last interval

            temporary[entity][keyword] += 1

    # Matplotlib 

    # So we count CAO, if ENTITY is both. Because we transformed CACL entities to CAO, 
    # we now have to display CAO
    # name is for the save location & which name to display on the graph
    if ENTITY == "both":
        ENTITY = "CAO"
        name = "both"
    else:
        name = ENTITY

    amount = len(all_actions[ENTITY])
    
    i = 0 # which bar it is. For x axis offset
    fig, ax = plt.subplots()
    axis_len = 0
    for event in all_actions[ENTITY]:
        ax.bar(
            np.array(dd_timestamps[ENTITY][event])+i/(amount+1),
            all_actions[ENTITY][event],
            width=1/(amount+1),
            label=event,
            align='edge'
        )
        axis_len = dd_timestamps[ENTITY][event][-1]
        i+=1

    ax.set_title('log: '+filename+'; entity: '+ name)
    ax.legend()

    ax.set_xticks(np.arange(0, axis_len+1, 1), minor=True)
    ax.set_xticks(np.arange(0, axis_len+1, 10))
    ax.grid(color='k', alpha=0.5, which='major')
    ax.grid(color='k', alpha=0.2, which='minor')


    fig.tight_layout()
    fig.set_size_inches(16, 12) # Size of the graph
    #plt.show()
    plt.savefig(name+'/'+filename[:-4]+'.png', dpi=(100))
    #print(all_actions['CACL'])

    plt.close()
    return num_d*weights[0] + num_i*weights[1] + level_a*weights[2] + level_f*weights[3]

if __name__ == "__main__":
    weighted_sum = main(sys.argv[1], [0.4, 0.3, 0.2, 0.1])
    print(weighted_sum)
