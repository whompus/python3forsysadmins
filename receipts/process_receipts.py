#!/usr/bin/env python3

import os
import glob
import json
import shutil

# create the processed dir
try:
    os.mkdir('./processed')
except OSError: # we are using OSError because it ecompasses all of the subclasses here: https://docs.python.org/3/library/exceptions.html#FileExistsError
    print("'processed' directory already exists")

# finds and returns file names themselves
# receipts = glob.glob('./new/receipt-[0-9]*.json') # replaced with some refactoring below

# initialize subtotal variable
subtotal = 0.0

# loop through each receipt that matches our glob and process it
for path in glob.iglob('./new/receipt-[0-9]*.json'): # using iglob to get one item at a time instead of everything, this allows us to load it into our for loop
    with open(path) as f:
        content = json.load(f) # use json.load to take readable object (f), and returns to use a serializable object, in this case, a dictionary object
        subtotal += float(content['value']) # because we are converting into a dictionary, we can read the 'value' key and return it's value
    # name = path.split("/")[-1] # "./new/receipt-1.json".split('/') will output a list: ['.', 'new', 'receipt-1.json'], and we are taking hte last item with [-1]
    # destination = f"./processed/{name}" # replaced with refactoring below
    destination = path.replace('new', 'processed')
    shutil.move(path, destination)
    print(f"moved '{path}' to '{destination}'")

# print("Receipt subtotal: $%.2f" % subtotal) # python2 interpolation syntax
print(f"Receipt subtotal: ${round(subtotal, 2)}")

