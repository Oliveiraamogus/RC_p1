#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *
import random
import sys

serverPort = int(sys.argv[1])
sockBuffer = 1024

fileName = "server"

def main():

    serverSocket = socket(AF_INET,SOCK_STREAM)   # create TCP welcoming socket
    serverSocket.bind(("", serverPort))

    serverSocket.listen(1)                      # begin listening for incoming TCP requests
    print("Server is running")

    while True:
        serverNumber = random.randint(1,100)

        connSocket, addr = serverSocket.accept()    # waits for incoming requests:
                                                    # new socket created on return
        print("Connected by: ", str(addr))


        with open(sys.argv[2], 'wb') as f:
          while True:
              chunk = connSocket.recv(sockBuffer) 
              f.write(chunk)  
              if not chunk:
                  break
        f.close()

        connSocket.close()      # close TCP connection:
                                # the welcoming socket continues

main()
