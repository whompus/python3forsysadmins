#!/usr/bin/env python3

import random
import os
import json

# count below is how many files or receipts we want to generate, if we don't specify, then it will generate 100
count = int(os.getenv("FILE_COUNT") or 100)
# list of words that is big
words = [word.strip() for word in open('/usr/share/dict/words').readlines()]

for identifier in range(count):
    # receipt amount
    amount = random.uniform(1.0, 1000)
    # receipt contents
    content = {
        # choose a random word from the words list
        'topic': random.choice(words),
        # takes whatever float is defined by amount, interpolates with %, .2 says how many decimal places to have, and f tells it that we are passing it a float
        'value': "%.2f" % amount 
    }
    with open(f'./new/receipt-{identifier}.json', 'w') as f:
        json.dump(content, f)