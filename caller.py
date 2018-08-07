import histogram
import os
import sys

# Read all files in this directory
files = os.listdir()
line = ""
weights = [0.4, 0.3, 0.2, 0.1]

# Read from the argv if user supplied. If not, use default values
try:
    argument = sys.argv[1]
except e:
    argument = ""

# Also count instances of actions, save them in text file
with open(argument+"weighted.txt", 'w') as f:
    for thing in files:
        # Create a histogram for every file with .log extension
        if thing[-3:] == 'log':
            if argument != "":
                line = str(histogram.main(thing, weights, ENTITY=argument))
            else:
                line = str(histogram.main(thing, weights))
            line = thing + "    " + line + "\n"
            f.write(line)
