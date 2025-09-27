
import os
import pickle
import threading
import sys
from socket import *
from Packet import *

socketBuffer = 512
dir_path = "." 

def workOnClient(socket, addr):
  #é suposto mandar sempre um packect com welcome 
  welMsg = "Welcome to " + str(addr) + " file server"
  welcomePacket = DAT(3, 1, welMsg.len(), welMsg) 
  socket.send(welcomePacket.dumps())
  #acho que temos de receber um ACK do client e só depois é comecamos a fazer packest de comandos
  while True:
  #vamos receber um packet  
    packet = Packet   
    packet = socket.recv(socketBuffer).loads()     
    opcode = packet.getCode()
    
    match opcode:
      case 1:
        if packet.getFilename() != "":
          print("file")
        else :
          for path in os.listdir(dir_path):
              # check if current path is a file
              if os.path.isfile(os.path.join(dir_path, path)):
                  res.append(path)

      case 4:
        print("oi")
      
    socket.close()
workOnClient()


def main():
  server_port = sys.argv[1] 

  serverSocket = socket(AF_INET,SOCK_STREAM)   # create TCP welcoming socket
  serverSocket.bind(("", server_port))

  serverSocket.listen() 
  #ligado e tal gostava de saber se retorna alguma coisa pq se falhar falta uma msg
  print("Server is running")
  ## acho q era suposto mandar uma mensagem para o client e recerber o ack packet do client maybe

  while (True):
    newSocket, addr = serverSocket.accept()
    #abrir a thread
    tid = threading.Thread(target= workOnClient, args= (newSocket, addr))
    tid.start()



main()
    
