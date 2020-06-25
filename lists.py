#!/usr/bin/env python3

users = [
    {'name': 'Mat', 'active': True, 'admin': True},
    {'name': 'Kevin', 'active': False, 'admin': True},
    {'name': 'James', 'active': True, 'admin': False}
]

line = 1

for user in users:
    prefix = f"{line} "
    if user['admin'] and user['active']:
        prefix += 'ACTIVE - (ADMIN) '
    elif user['active']:
        prefix += 'ACTIVE - '
    elif user['admin']:
        prefix += '(ADMIN) '
    
    print(prefix + user['name'])
    line += 1