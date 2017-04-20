"""
Author: Jacob Bieker 2017

Using suffix tree for searching in filename

"""
from McM_suffix_tree_build import built_tree
import os, sys, time

if __name__ == "__main__":
    filename = sys.argv[0]
    search_string = sys.argv[1]

    with open(filename, "r") as datafile:
        data = datafile.read().replace('\n', '')
        # Build tree from data file
        start = time.time()
        tree = built_tree(data, False)
        end = time.time()
        print("Construction Time")
        print(end - start)
        print("Size per character (On average): ")
        print(sys.getsizeof(data)/len(data))
        
