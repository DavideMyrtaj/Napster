import uuid
import socket, sys
import hashlib
import threading
import os,random
#from os import fork
from os.path import exists

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
def Resize(stringa, dim):
        tmp=""
        for n in range(0,dim-len(stringa)):
            tmp+="0"
        tmp+=stringa
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
    porta=Resize(porta,5)
    client=SendData(f"LOGI{ip}{porta}",ipDirectory,50000)
    client.recv(4)
    return client.recv(16).decode(),porta
#metodo che invia al server la richiesta di condivisione del file
def Aggiungi(sessionID,filename):
    md5 = calcoloMD5(f"{percorso}/{filename}")
    print(f"MD5 del file {filename}: {md5}")
    client=SendData(f"ADDF{sessionID}{md5}{filename.ljust(100)}",ipDirectory,50000)
    client.recv(4)
    return client.recv(3).decode(),filename,md5
    
def SendData(send,ip,port):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((ip,port))
    except:
        print("il server non è raggiungibile, riprova più tardi")
        exit()
        
    client.send(str(send).encode())
    return client
def Ricerca(sessionid, descrizione):
    client=SendData(f"FIND"+sessionid+descrizione,ipDirectory,50000)
    client.recv(4)
    nmd5=int(client.recv(3).decode())
    print(f"ci sono {nmd5} file che combaciano con '{descrizione}'\n")
    for n in range(0,nmd5):
        md5=client.recv(32).decode()
        name=client.recv(100).decode()
        tot=int(client.recv(3).decode())
        print(f"MD5: {md5} | Nome: {name}\n")
        for i in range(0,tot):
            print(f"\tIP: {client.recv(15).decode()} | PORTA: {int(client.recv(5).decode())}")
    client.close()
    

def showFile(path):
    files = os.listdir(path)
    for i in files:
        print(i)

def InvioFile(peer,file):
    send="ARET"
    if(not exists(percorso)):
        peer.send("ARET"+"000000")
        return
    fd = os.open(filename, os.O_RDONLY)
    dim=os.path.getsize(file)
    filechunk=dim//4096
    last=dim%4096
    if(last!=0):filechunk+=1
    send+=Resize(filechunk,6)
    peer.send(send.encode())
    send=""
    for n in range(0,dim//4096):
        send+="04096"
        send+=os.read(fd,4096).decode()
        peer.send(send.encode())
        send=""
    if(last!=0):
        send+=Resize(last,5)
        send+=os.read(fd,4096).decode()
        peer.send(send.encode())
    fd.close()
    peer.close()
    

    


def AvvioAscoltoServer(porta):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("",int(porta)))
    sock.listen(10)
    while True:
        client,addr= sock.accept()
        pid=0
        if(pid==0):
            richiesta=client.recv(4).decode()
            if(richiesta=="RETR"):
                md5=client.recv(32).decode()
                for n in range(0,len(listaFileCondivisi)):
                    if(listaFileCondivisi[n][1]==md5):
                        InvioFile(client,percorso+"/"+listaFileCondivisi[n][0])
                        break
            client.close()

def DownloadFilePeer(ip,port,md5):
    send="RETR"+md5
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((ip,int(port)))
    except:
        print("il server non è raggiungibile, riprova più tardi")
        
        return
    client.recv(4)
    pid=0
    if(pid==0):
        chunk=client.recv(6).decode()
        fd = os.open("download/"+md5, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o777)
        for n in range(0,chunk):
            buf=client.recv(int(client.recv(5).decode()))
            os.write(fd,buf)
        os.close(fd)
        print("ricevuto il file "+md5)
        client.close()
        exit()


def AggiornaListaLocale():
    files = os.listdir(percorso)





ipDirectory="192.168.1.79"

sessionid, porta=Login(str(random.choice(range(49152,65536))))
if(sessionid=="0000000000000000"):
    print("Si è verificato un errore durante il processo di Log-in")
    exit()

print(f"Il tuo sessionID = {sessionid}")


server_client=threading.Thread(target=AvvioAscoltoServer,args=(porta,))
server_client.start()
listaFileCondivisi=[]
percorso = "file_condivisi"



while True:
    scelta = input("Scegli azione da svolgere: \n1)Aggiorna file condivisi\n2)Ricerca file\n3)Ricevi file\n4)Logout\n")
    if(scelta == "1"):
        files = os.listdir(percorso)
        for i in files:
            nfile,filename,md5=Aggiungi(sessionid,i)
            print(f"sono presenti {int(nfile)} copie del file {filename}")
            listaFileCondivisi.append([filename,md5])

    elif(scelta == "2"):
        daCercare = input("scegli il file da cercare")
        Ricerca(sessionid,daCercare)

    elif(scelta == "3"):
        ipPeer=input("Inserisci l'ip del peer dal quale scaricare")
        portaPeer=input("Inserisci la porta del peer")
        md5Download=input("inserisci l'md5 del file da scaricare")
        DownloadFilePeer(ipPeer,portaPeer,md5Download)


    elif(scelta == "4"):
        print("Inizio logout in corso")

    else:
        print("Opzione non valida")


