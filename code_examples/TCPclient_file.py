#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *
import sys

serverName = sys.argv[1]            # server name
serverPort = int(sys.argv[2])                  # socket server port number
sockBuffer = 512                   # socket buffer size

def main():
  try:
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    clientSocket.connect((serverName, serverPort))   # open TCP connection
  except ConnectionRefusedError:
    print("Connection Refused")
    sys.exit()

  print("Connect to server")
  print(clientSocket.recv(sockBuffer).decode()) 

  sentence = [""]
  while (sentence[0] != "end") :
    try:
      sentence = (input ("Command: ")).split()
      match sentence[0]:
        case "dir":
          clientSocket.send(["RRQ", ""])
          while True:
              chunk = clientSocket.recv(sockBuffer).decode()
              print(chunk)
              if not chunk:
                  break
        case "get":
          sentence[0] = "RRQ"
          clientSocket.send(sentence)
          for file in sentence:
            with open(file, 'wb') as f:
              while True:
                chunk = clientSocket.recv(sockBuffer) 
                f.write(chunk)  
                if not chunk:
                    break
            f.close()
        case "end":
          print("Connection close, client ended")
        case _:
          print("Unknown command")

      f.close()
      # take input
    except KeyboardInterrupt:
        print("Exiting!")
        break
    print("client done")

    clientSocket.close()            # close TCP connection

main()
