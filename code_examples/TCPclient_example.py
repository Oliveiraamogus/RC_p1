#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *

serverName = "172.17.0.2"            # server name
serverPort = 12000                  # socket server port number
sockBuffer = 2048 * 2                  # socket buffer size

def main():



    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    clientSocket.connect((serverName, serverPort))   # open TCP connection

    sentence = input ("Enter Name: ")
    val = int(input("Enter Number: "))
   # take input

    clientSocket.send(sentence.encode())             # send user's sentence
                                                     # over TCP connection
    clientSocket.send(val.to_bytes(2, 'big'))             # send user's value
                                                     # over TCP connection



    val = clientSocket.recv(sockBuffer)     # read a value
                                                        # received from client
    val = int.from_bytes(val, 'big')
    
    print("Message received: ", val)
    
    clientSocket.close()            # close TCP connection

main()
