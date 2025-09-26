#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *
import sys

args = (sys.argv[1]).split(':')

serverName = args[0]            # server name
serverPort = int(args[1])                  # socket server port number
sockBuffer = 1024                   # socket buffer size

def main():

  nameInServer = args[2]
  

  clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
  clientSocket.connect((serverName, serverPort))   # open TCP connection

  with open(sys.argv[2], 'rb') as f:
    while True:
        chunk = f.read(sockBuffer)
        if not chunk:
            break
        else:
          clientSocket.send(chunk)
  f.close()
  # take input
  print("client done")

  clientSocket.close()            # close TCP connection

main()
