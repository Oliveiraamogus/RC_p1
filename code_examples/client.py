#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *
from Packet import *
import sys
import pickle

serverName = sys.argv[1]            # server name
serverPort = int(sys.argv[2])                  # socket server port number
sockBuffer = 1024              # socket buffer size


def dir(clientSocket):
  clientSocket.send(pickle.dumps(RRQ("")))
  while True:
      chunk = pickle.loads(clientSocket.recv(sockBuffer))
      print(chunk.getData())

      #eu tenho quase a certeza q e preciso o decode, a data vai ser array de bytes, e o dir é pa listar no
      # standard output o nome, como string, por isso pa passar o array de bytes pa string .decode()
      clientSocket.send(pickle.dumps(ACK(chunk.getBlock())))
      if chunk.getSize() == 0:#acho que é suposto veres se está vazio a data do chunk
          #porque o ultimo que mando é um dat vazio (eles pediram no enunciado)
          break



def get(clientSocket, filenames):
  clientSocket.send(pickle.dumps(RRQ(filenames[1])))
  with open(filenames[2], 'a') as f:
    while True:
      chunk = pickle.loads(clientSocket.recv(sockBuffer))
      f.write(chunk.getData())
      clientSocket.send(pickle.dumps(ACK(chunk.getBlock())))
      if chunk.getSize() < 512:
        break
  f.close()



def main():
  try:
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    clientSocket.connect((serverName, serverPort))   # open TCP connection
  except ConnectionRefusedError:
    print("Connection Refused")
    sys.exit()

  print("Connect to server")
  print((pickle.loads((clientSocket.recv(sockBuffer))).getData())) 
  clientSocket.send(pickle.dumps(ACK(1)))
  sentence = [""]
  while (sentence[0] != "end") :
    try:
      sentence = (input ("Command: ")).split()
      match sentence[0]:
        case "dir":
          dir(clientSocket)
        case "get":
          get(clientSocket, sentence)
        case "end":
          clientSocket.close()            # close TCP connection
          print("Connection close, client ended")
        case _:
          print("Unknown command")

      # take input
    except KeyboardInterrupt:
        print("Exiting!")
        break


main()
