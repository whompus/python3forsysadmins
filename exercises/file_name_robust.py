#!/usr/bin/env python3

# how the f does this loop??
def get_file_name(reprompt=False):
    if reprompt:
        print("Please enter a file name.")

    file_name = input("Destination file name: ").strip()
    return file_name or get_file_name(True)

file_name = get_file_name()

print(f"Please enter your content. Entering an empty line will write the content to {file_name}:\n")

with open(file_name, 'w') as f:
    eof = False
    lines = []

    # while eof is False, take input, remove whitespace, and append to list, 
    # if empty line (where line.strip() is false), flip eof to True and exit loop
    while not eof:
        line = input()
        if line.strip():
            lines.append(f"{line}\n")
        else:
            eof = True

    f.writelines(lines)
    print(f"Lines written to {file_name}")