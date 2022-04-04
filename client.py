import uuid
import socket, sys

from paramiko import SSHClient
def prepIp():
    ip=socket.gethostbyname(socket.gethostname())
    ip=ip.split(".")
    for n in range(0,len(ip)):
        group=""
        for i in range(0,3-len(ip[n])):
            group+="0"
        group+=ip[n]
        ip[n]=group
    return ".".join(ip)
def prepPort(porta):
    tmp=""
    for n in range(0,5-len(porta)):
        tmp+="0"
    tmp+=porta
    
    return tmp

def Login(porta):
    ip=prepIp()
    porta=prepPort(porta)
    return ip,porta

client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip,porta =Login("9785")
client.connect(("localhost",50000))
client.send(f"LOGI{ip}{porta}".encode())
client.recv(4)
sessionid=client.recv(16).decode()
print(sessionid)
client.close()








