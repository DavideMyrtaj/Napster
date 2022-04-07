import uuid
import socket, sys
import hashlib
import os

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

def Aggiungi(sessionID, descrizione, filename): #da modificare ---> il metodo manda tutti i file in una volta sola
    md5 = calcoloMD5(filename)
    print(f"MD5 del file {filename}: {md5}")
    print(f"Descrizione del file: {descrizione}")
    client=SendData(f"ADDF{sessionID}{md5}{filename}")
    

def SendData(send):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("localhost",50000))
    client.send(str(send).encode())
    return client

def showFile(path):
    files = os.listdir(path)
    for i in files:
        print(i)

ip,porta = Login("9785")


client=SendData(f"LOGI{ip}{porta}")
client.recv(4)
sessionid=client.recv(16).decode()
print(f"Il tuo sessionID = {sessionid}")
scelta = input("Scegli azione da svolgere: \n1)Aggiungi file\n2)Cancella file\n3)Ricerca file\n4)Ricevi file\n5)Logout")
if(scelta == "1" or scelta == "login"):
    file = input("Inserisci il nome del file: ")
    descrizione = input("Inserisci una breve descrizione del file: ")
    Aggiungi(sessionid, "file di prova", "server.py")

elif(scelta == "2" or scelta == "cancella"):
    showFile("path")
    daCancellare = input("Scegli il file da cancellare: ")

elif(scelta == "3" or scelta == "ricerca"):
    daCercare = input("scegli il file da cercare")

elif(scelta == "4" or scelta == "ricevi"):
    daRicevere = input("Scegli il file da ricevere")

elif(scelta == "5" or scelta == "logout"):
    print("Inizio logout in corso")

else:
    print("Opzione non valida")
    exit(1)

client.close()

