#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file_name', help='the file to read')
parser.add_argument('line_number', type=int, help='the line to print from the file')

args = parser.parse_args()

try:
    lines = open(args.file_name, 'r').readlines()
    line = lines[args.line_number - 1]
except IndexError:
    print(f"Error: file '{args.file_name}' doesn't have {args.line_number} lines.")
except IOError as err:
    print(f"Error: {err}")
else:
    print(line)