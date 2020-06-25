#!/usr/bin/env python3

file_name = input("Please enter a file name to save the content: ").strip()

def write_to_file(filename):
    while True:
        line = input("Please enter something to write into the file (empty line exits): ")
        if not line.strip():
            break
        else:
            with open(filename, 'a') as f:
                f.write(f"{line}\n")

write_to_file(file_name)
