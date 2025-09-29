"""
@author: Beatriz Ramos (68030)
@author: Manuel Oliveira ()
"""

import os
import threading
import sys
import pickle
from socket import *
from Packet import *

socketBuffer = 1024   # socket buffer size
blockSize = 512       # block size
dir_path = "."        # current path 

class ClientProtocolError(Exception):
  pass

def workOnClient(socket, addr):
  # send welcoming packet with server identification 
  welMsg = "Welcome to " + str(addr) + " file server"
  welcomePacket = DAT(1, len(welMsg), welMsg) 
  socket.send(pickle.dumps(welcomePacket))
  # receiving client's ACK packet
  pickle.loads(socket.recv(socketBuffer))
  while True:
    try:
      # receiving client's RRQ packets for command GET or DIR
      packet = pickle.loads(socket.recv(socketBuffer))
      # checking if it´s a RRQ packet
      if not isinstance(packet, RRQ):
        raise ClientProtocolError
      
      if packet.getFilename() != "": # GET command
            try:
              # openning the file
              with open(packet.getFilename(), 'r') as f:
                fsize = os.path.getsize(packet.getFilename()) # get file size
                blockN = (fsize // blockSize) + 1 # calculating how many blocks we'll need for a file with fsize
                for i in range(int(blockN)):
                  data = f.read(blockSize)
                  datP = DAT(i + 1, len(data), data)
                  socket.send(pickle.dumps(datP)) # sending the DAT packet
                  ackP = pickle.loads(socket.recv(socketBuffer)) # receiving the ACK packet
                  # checking for a macth in block numbers and protocol errors
                  if not isinstance(ackP, ACK) or i + 1 != ackP.getBlock():
                    raise ClientProtocolError
                      
            except FileNotFoundError:
              errP = ERR("File not found")
              socket.send(pickle.dumps(errP)) # sending ERR packet
            except ClientProtocolError:
              print("Protocol error,Connection closed")
              socket.close() # close TCP connection


      else : # DIR command
      
        try:
          i = 1
          for path in os.listdir(dir_path):
              if os.path.isfile(os.path.join(dir_path, path)): # check if current path is a file
                  p = DAT(i, len(path),path)
                  socket.send(pickle.dumps(p)) # sending the DAT packet
                  ackP = pickle.loads(socket.recv(socketBuffer)) # receiving the ACK packet
                  # checking for a macth in block numbers and protocol errors
                  if isinstance(ackP, ACK) and i == ackP.getBlock():
                    i = ackP.getBlock() + 1
                  else :
                    raise ClientProtocolError
            
          p = DAT(i, 0, "")
          socket.send(pickle.dumps(p)) #send empty DAT packet to signal that all information has been transmitted
        except ClientProtocolError:
          print("Protocol error,Connection closed")
          socket.close()# close TCP connection
        
    except EOFError: #####Para quê esta drena?????
      break
    except ClientProtocolError:
            print("Protocol error,Connection closed")
            socket.close() # close TCP connection
  socket.close() # close TCP connection


def main():
  server_port = int(sys.argv[1]) # socket server port number

  try:
    serverSocket = socket(AF_INET,SOCK_STREAM) # create TCP welcoming socket
    serverSocket.bind(("", server_port))
  except ConnectionRefusedError:
    print("Unable to start server")
    sys.exit()

  serverSocket.listen() # begin listening for incoming TCP requests
  print("Server is running")
  
  while True:
    newSocket, addr = serverSocket.accept() # waits for incoming requests and new socket is created on return
    tid = threading.Thread(target= workOnClient, args= (newSocket, addr)) # creating a thread to handle client
    tid.start()

main()
    
