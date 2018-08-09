import scatter_plot
import os
import sys

# Read all files in this directory
files = os.listdir()
line = ""

# Read from the argv if user supplied. If not, use default values
try:
    argument = sys.argv[1]
except Exception:
    argument = ""

# Also count instances of actions, save them in text file
for thing in files:
    # Call scatter plot for every file with .log extension
    if thing[-3:] == 'log':
        if argument != "":
            scatter_plot.main(thing, ENTITY=argument)
        else:
            scatter_plot.main(thing)
