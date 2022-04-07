from fileinput import filename
import uuid
import socket, sys
import hashlib

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

def calcoloMD5(filename):
    file = open(filename, 'rb')
    stringaMD5 = hashlib.md5()
    dati = 0
    while dati != b'':
        dati = file.read()
        stringaMD5.update(dati)

    stringaMD5 = stringaMD5.hexdigest().upper()
    return stringaMD5

def Login(porta):
    ip=prepIp()
    porta=prepPort(porta)
    return ip,porta

def Aggiungi(sessionID, descrizione, filename):
    md5 = calcoloMD5(filename)
    print(f"MD5 del file {filename}: {md5}")
    print(f"Descrizione del file: {descrizione}")
    client.send(f"ADDF{sessionID}.{md5}.{filename}")
    

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip,porta = Login("9785")
client.connect(("localhost",50000))
client.send(f"LOGI{ip}{porta}".encode())
client.recv(4)
sessionid=client.recv(16).decode()
print(f"Il tuo sessionID = {sessionid}")
scelta = input("Scegli azione da svolgere: \n1)Aggiungi file\n2)altre opzioni\n")
if(scelta == "1" or scelta == "aggiungi"):
    file = input("Inserisci il nome del file: ")
    descrizione = input("Inserisci una breve descrizione del file: ")
    Aggiungi(sessionid, descrizione, file)

client.close()
