
import os
import threading
import sys
from socket import *
from Packet import *
from pickle import *

socketBuffer = 512
dir_path = "." 

def workOnClient(socket, addr):
  #é suposto mandar sempre um packect com welcome 
  welMsg = "Welcome to " + str(addr) + " file server"
  welcomePacket = DAT(1, welMsg.len(), welMsg) 
  socket.send(welcomePacket.dumps())
  #acho que temos de receber um ACK do client e só depois é comecamos a fazer packets de comandos
  socket.recv(socketBuffer).loads()

  while True:
  #vamos receber um packet  
    #packet = Packet  
    # é possivel que o codigo embaixo não vá reconher que vamos fazer loads a uma packet 
    packet = socket.recv(socketBuffer).loads()     
    #ver se tenho de fazer um isinstance() de packet para poder usar o metodo getcode
    opcode = packet.getCode()
    
    match opcode:
      case 1: #RRQ packet
        if packet.getFilename() != "": #comando GET
          # se o file não existir tenho de mandar um packet de erro e fechar a cena 
          # reclamar se for enviado uma packet que não é ack
          try:
            with open(sys.argv[2], 'wb') as f:
              while True:
                chunk = socket.recv(socketBuffer) 
                if not chunk:
                    break
                f.write(chunk)  
          except:
            errP = ERR("File not found")
            socket.send(errP.dumps())

        else : #comando DIR
          i = 1
          for path in os.listdir(dir_path):
              # check if current path is a file
              if os.path.isfile(os.path.join(dir_path, path)):
                  p = DAT(i, path.len(),path)
                  socket.send(p.dumps())
                  ackP = socket.recv(socketBuffer).loads()
                  ##falta reclamar se ele mandar um packet que não é ack
                  #se o i não for igual ao bloco do packet recebebido devo dar erro ou fechar alguma coisa
                  if isinstance(ackP, ACK) and i == ackP.getBlock() and ackP.getCode() == 3:
                    i = ackP.getBlock() + 1
                  else :
                    ##acho que tenho tirar a parte de enviar o packet de erro
                    errP = ERR("Protocol error, Connection closed")
                    socket.send(errP.dumps())
                    socket.close()
          
          # mandar o packect vazio para saber que terminou a comunicação
          p = DAT(i, 0, "")
          socket.send(p.dumps())


      case 4: #ACK packet  lol afinal acho que não preciso disto e provavelmente nem do case
        print("oi")
      
    socket.close()
workOnClient()


def main():
  server_port = sys.argv[1] 

  try:
    serverSocket = socket(AF_INET,SOCK_STREAM)   # create TCP welcoming socket
    serverSocket.bind(("", server_port))
  except:
    print("Unable to start server")
    sys.exit()

  serverSocket.listen() 
  #ligado e tal gostava de saber se retorna alguma coisa pq se falhar falta uma msg
  print("Server is running")
  
  while (True):
    newSocket, addr = serverSocket.accept()
    #abrir a thread
    tid = threading.Thread(target= workOnClient, args= (newSocket, addr))
    tid.start()

main()
    
