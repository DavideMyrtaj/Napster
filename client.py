import uuid
import socket, sys


client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("localhost",50000))
client.send(f"LOGI{socket.gethostbyname(socket.gethostname())}{50789}".encode())
client.close()








