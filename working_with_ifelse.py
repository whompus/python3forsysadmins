#!/usr/bin/env python3

user = {
    'admin': True,
    'active': True,
    'name': 'Mat'
}

prefix = ""

if user['active'] and user['admin']:
    prefix = "ACTIVE - (ADMIN) "
elif user['admin']:
    prefix = "(ADMIN) "
elif user['active']:
    prefix = "ACTIVE - "

print(prefix + user['name'])