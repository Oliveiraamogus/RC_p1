"""
@author: Beatriz Ramos (68030)
@author: Manuel Oliveira ()
"""
from socket import *
from Packet import *
import sys
import pickle

serverName = sys.argv[1]            # server name
serverPort = int(sys.argv[2])       # socket server port number
sockBuffer = 1024                   # socket buffer size
blockSize = 512       # block size


def dir(clientSocket): # DIR command
  clientSocket.send(pickle.dumps(RRQ(""))) # sending RRQ packet
  while True:
      chunk = pickle.loads(clientSocket.recv(sockBuffer)) # receiving DAT packet
      print(chunk.getData())

      clientSocket.send(pickle.dumps(ACK(chunk.getBlock()))) # sending ACK packet
      if chunk.getSize() == 0: # the command ends when the client receives an empty DAT packet
          break



def get(clientSocket, filenames): # GET command
  clientSocket.send(pickle.dumps(RRQ(filenames[1]))) # sending RRQ packet with the remote file name
  with open(filenames[2], 'a') as f: # creating and openning the local file
    while True:
      chunk = pickle.loads(clientSocket.recv(sockBuffer)) # receiving DAT packet
      f.write(chunk.getData()) # writing on the loacal file
      clientSocket.send(pickle.dumps(ACK(chunk.getBlock()))) # sending ACK packet
      if chunk.getSize() < blockSize: # the command ends when the client receives a DAT packet with less than 512 bytes
        break
  f.close()
  ### não estamos a ler possiveis packets do tipo ERR



def main():
  try:
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    clientSocket.connect((serverName, serverPort))   # open TCP connection
  except ConnectionRefusedError:
    print("Connection Refused")
    sys.exit()

  print("Connect to server")
  print((pickle.loads((clientSocket.recv(sockBuffer))).getData())) # receiving server's welcoming DAT packet
  clientSocket.send(pickle.dumps(ACK(1))) # sending ACK packet
  sentence = [""] 
  #### acaba de commentar esta parte pls
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
