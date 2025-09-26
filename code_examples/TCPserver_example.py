#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *
import random

serverPort = 12000
sockBuffer = 2048 * 2

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

        sentence = connSocket.recv(sockBuffer).decode()     # read a sentence of bytes
                                                            # received from client

        val = connSocket.recv(sockBuffer)     # read a value
                                                         # received from client
        val = int.from_bytes(val, 'big')
        result = val + serverNumber

        print("Data from connected user: ", sentence)       # display received sentence
        print("User Number: ", val)
        print("Server number: ", serverNumber)
        print("Result: ", result)



        connSocket.send(result.to_bytes(2, 'big'))             # send modified sentence over
                                                            # TCP connection

        connSocket.close()      # close TCP connection:
                                # the welcoming socket continues

main()
