#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  23 13:42:42 2025

@author: carmen
Catch a keyboard interrupt
"""
import time

def main():
    print("Starting ...")
    while True:
        try:
            print(".", end=' ',flush=True)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting!")
            break
    print("Ending ")

main()
