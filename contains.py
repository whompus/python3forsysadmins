#!/usr/bin/env python3

# take a word as input, search words list for that word

import argparse

parser = argparse.ArgumentParser(description='Search for words including partial word')
parser.add_argument('snippet', help='partial (or complete) string to search for in words')

args = parser.parse_args()
snippet = args.snippet.lower()

with open('/usr/share/dict/words') as f:
    words = f.readlines()

# matches = []

# for word in words:
#     if snippet in word.lower():
#         matches.append(word)

matches = [word.strip() for word in words if snippet in word.lower()] # list comprehension instead of block above, strip() removes whitespace
num_matches = str(len(matches))

print(matches)
print(f'\nFound {num_matches} partial or exact matches for \'{snippet}\'')