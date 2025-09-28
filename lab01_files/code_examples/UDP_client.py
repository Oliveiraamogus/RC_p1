import socket

msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("172.17.0.2", 20001) # container addr 
bufferSize          = 1024

 # Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send the message to server using the UDP socket created
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)

message = bytesAddressPair[0].decode()
address = bytesAddressPair[1]

serverMsg  = "Message from Server: {}".format(message)
serverAddr = "Server (IP Address, Port): {}".format(address)

print(serverMsg)
print(serverAddr)
