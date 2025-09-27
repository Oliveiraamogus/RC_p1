#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *
from Packet import Packet, RRQ, DAT, ACK, ERR
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
  print(clientSocket.recv(sockBuffer)) 

  sentence = [""]
  while (sentence[0] != "end") :
    try:
      sentence = (input ("Command: ")).split()
      match sentence[0]:
        case "dir":
          clientSocket.send(RRQ(""))
          while True:
              chunk = clientSocket.recv(sockBuffer)
              print(chunk.getData().decode())
              clientSocket.send(ACK(chunk.getBlock()))
              if chunk.getBlock() == null:
                  break
        case "get":
          sentence.pop(0) #remover o "get"
          clientSocket.send(RRQ(sentence))
          for file in sentence:
            with open(file, 'wb') as f:
              while True:
                chunk = clientSocket.recv(sockBuffer) 
                f.write(chunk.getData())  
                clientSocket.send(ACK( chunk.getBlock()))
                if chunk.getBlock() == null:
                  break
            f.close()
        case "end":#aqui não devias fazer lg socket.colse()??
          print("Connection close, client ended")
        case _:
          print("Unknown command")

      # take input
    except KeyboardInterrupt:
        print("Exiting!")
        break
    print("client done")

    clientSocket.close()            # close TCP connection

main()
