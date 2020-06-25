#!/usr/bin/env python3

message = input("What message would you like to echo? ")
num_message = input("How many times would you like to repeat the message? (default is 1): ")

if num_message:
    num_message = int(num_message)
else:
    num_message = 1

def multi_echo(message, num_message):
    while num_message > 0:
        print(message)
        num_message -= 1

multi_echo(message, num_message)