"""
@author: Beatriz Ramos (68030)
@author: Manuel Oliveira (68547)
"""
from socket import *
import os
import sys
import pickle

serverName = sys.argv[1]            # server name
serverPort = int(sys.argv[2])       # socket server port number
sockBuffer = 1024                   # socket buffer size
blockSize = 512       # block size

RRQ = 1
DAT = 3
ACK = 4
ERR = 5

class ClientProtocolError(Exception):
  pass

def dir(clientSocket): # DIR command
  clientSocket.send(pickle.dumps((RRQ, ""))) # sending RRQ packet
  expected_block_number = 1
  while True:
    try:
      chunk = pickle.loads(clientSocket.recv(sockBuffer)) # receiving DAT packetif chunk[0] == ERR:
      if chunk[1] != expected_block_number :
        raise ClientProtocolError
      else :
        expected_block_number += 1
      if chunk[2] == 0: # the command ends when the client receives an empty DAT packet
          break
      else:
        print(chunk[3])
        clientSocket.send(pickle.dumps((ACK, chunk[1]))) # sending ACK packet
    except ClientProtocolError:
      print("Protocol error,Connection closed")
      clientSocket.close() # close TCP connection



def get(clientSocket, filenames): # GET command
  try:
    with open(filenames[2], 'x') as f: # creating and openning the local file
      clientSocket.send(pickle.dumps((RRQ, filenames[1]))) # sending RRQ packet with the remote file name
      expected_block_number = 1
      while True:
        try:
          chunk = pickle.loads(clientSocket.recv(sockBuffer)) # receiving DAT packet
          if chunk[0] == ERR:
            os.remove(filenames[2])
            print("File not found")
            break
          f.write(chunk[3]) # writing on the local file
          clientSocket.send(pickle.dumps((ACK, chunk[1]))) # sending ACK packet
          if chunk[1] != expected_block_number :
            raise ClientProtocolError
          else :
            expected_block_number += 1
          if chunk[2] < blockSize: # the command ends when the client receives a DAT packet with less than 512 bytes
            print("File transfer completed")
            break
        except ClientProtocolError:
          print("Protocol error,Connection closed")
          clientSocket.close() # close TCP connection
    f.close()
  except FileExistsError:
    pass



def main():
  try:
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    clientSocket.connect((serverName, serverPort))   # open TCP connection
  except ConnectionRefusedError:
    print("Connection Refused")
    sys.exit()

  print("Connect to server")
  print((pickle.loads(clientSocket.recv(sockBuffer)))[3]) # receiving server's welcoming DAT packet
  clientSocket.send(pickle.dumps((ACK, 1))) # sending ACK packet
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
      clientSocket.close()            # close TCP connection
      break


main()
