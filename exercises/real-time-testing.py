#!/usr/bin/env python3

import time

timer = 0

while True:
    try:
        # real_time = time.strftime(" :%S", localtime())
        print(f'time elapsed: {timer} (press ctrl+c to stop)', end='\r')
        timer += 1
        time.sleep(1)
    except KeyboardInterrupt:
        total_time = timer - 1 
        print('\b\b\r')
        print(f'\n total time: {total_time} seconds')
        break