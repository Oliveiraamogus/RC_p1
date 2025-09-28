
import os
import threading
import sys
import pickle
from socket import *
from Packet import *
from pickle import *

socketBuffer = 512
dir_path = "." 

class ClientProtocolError(Exception):
  pass

def workOnClient(socket, addr):
  #é suposto mandar sempre um packect com welcome 
  welMsg = "Welcome to " + str(addr) + " file server"
  welcomePacket = DAT(1, len(welMsg), welMsg) 
  socket.send(pickle.dumps(welcomePacket))
  #acho que temos de receber um ACK do client e só depois é comecamos a fazer packets de comandos
  pickle.loads(socket.recv(socketBuffer))
  while True:
    try:
    #vamos receber um packet  
      #packet = Packet  
      # é possivel que o codigo embaixo não vá reconher que vamos fazer loads a uma packet 
      packet = pickle.loads(socket.recv(socketBuffer))
      #ver se tenho de fazer um isinstance() de packet para poder usar o metodo getcode
      opcode = packet.getCode()
      
      match opcode:
        case 1: #RRQ packet
          if packet.getFilename() != "": #comando GET
            # se o file não existir tenho de mandar um packet de erro e fechar a cena 
            # reclamar se for enviado uma packet que não é ack
            try:
              
              with open(packet.getFilename(), 'rb') as f:
                fsize = os.path.getsize(packet.getFilename())
                drenas = fsize % socketBuffer
                blockN = 0
                if drenas == 0 :
                  blockN = fsize / socketBuffer
                else : 
                  blockN = (fsize // socketBuffer) + 1
                print(fsize // socketBuffer)
                print(fsize)
                for i in range(int(blockN)):
                  print("Reading...!")
                  data = f.read(socketBuffer)
                  datP = DAT(i + 1, len(data), data)
                  socket.send(pickle.dumps(datP))
                  ackP = pickle.loads(socket.recv(socketBuffer))
                  ##falta reclamar se ele mandar um packet que não é ack
                  #se o i não for igual ao bloco do packet recebebido devo dar erro ou fechar alguma coisa
                  if not isinstance(ackP, ACK) and i + 1 != ackP.getBlock():
                    raise ClientProtocolError
                      
            except FileNotFoundError:
              errP = ERR("File not found")
              socket.send(pickle.dumps(errP))
            except ClientProtocolError:
              print("Protocol error,Connection closed")
              socket.close()


          else : #comando DIR
          #MUDAR ERSTA MERDA PARA TRY EXCEPT 
            i = 1
            for path in os.listdir(dir_path):
                # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    p = DAT(i, len(path),path)
                    socket.send(pickle.dumps(p))
                    ackP = pickle.loads(socket.recv(socketBuffer))
                    ##falta reclamar se ele mandar um packet que não é ack
                    #se o i não for igual ao bloco do packet recebebido devo dar erro ou fechar alguma coisa
                    if isinstance(ackP, ACK) and i == ackP.getBlock():
                      i = ackP.getBlock() + 1
                    else :
                      socket.close()
            
            # mandar o packect vazio para saber que terminou a comunicação
            p = DAT(i, 0, "")
            socket.send(pickle.dumps(p))
        
    except EOFError:
      break
  socket.close()


def main():
  server_port = int(sys.argv[1]) 

  try:
    serverSocket = socket(AF_INET,SOCK_STREAM)   # create TCP welcoming socket
    serverSocket.bind(("", server_port))
  except ConnectionRefusedError:
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
    
