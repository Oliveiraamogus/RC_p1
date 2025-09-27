#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cpm
"""
from socket import *
from Packet import *
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
  #acho que falta mandar um pacote ack
  sentence = [""]
  while (sentence[0] != "end") :
    try:
      sentence = (input ("Command: ")).split()
      match sentence[0]:
        case "dir":
          clientSocket.send(RRQ(""))
          while True:
              chunk = clientSocket.recv(sockBuffer)
              print(chunk.getData().decode())#acho que não precisas de usar o decode encode apenas o loads() e dumps()
              #decode encode acho que é só para strings como o nosso chunk vai ser um objeto usas a 
              # sereialização do pickle que transforma o objeto em bytes pelo menos foi o que percebi
              clientSocket.send(ACK(chunk.getBlock()))
              if chunk.getBlock() == null:#acho que é suposto veres se está vazio a data do chunk
                  #porque o ultimo que mando é um dat vazio (eles pediram no enunciado)
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
