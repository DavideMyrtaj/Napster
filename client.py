import signal
import uuid
import socket, sys
import hashlib
import threading
import os,random
from pathlib import Path
#from os import fork
from os.path import exists

def prepIp(ip):
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
    ip=prepIp(socket.gethostbyname(socket.gethostname()))
    porta=Resize(str(porta),5)
    client=SendData(f"LOGI{ip}{porta}",ipDirectory,80)
    client.recv(4)
    return client.recv(16).decode(),porta
#metodo che invia al server la richiesta di condivisione del file
def Aggiungi(sessionID,filename):
    md5 = calcoloMD5(f"{percorso}/{filename}")
    print(f"MD5 del file {filename}: {md5}")
    client=SendData(f"ADDF{sessionID}{md5}{filename.ljust(100)}",ipDirectory,80)
    client.recv(4)
    totfile=client.recv(3).decode()
    client.close()
    return totfile,filename,md5
    
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
    client=SendData(f"FIND"+sessionid+descrizione,ipDirectory,80)
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
    if(not Path(file).is_file()):
        peer.send(("ARET"+"000000").encode())
        return
    fd = os.open(file, os.O_RDONLY)
    dim=os.path.getsize(file)
    filechunk=dim//4096
    last=dim%4096
    if(last!=0):filechunk+=1
    send+=Resize(str(filechunk),6)
    peer.send(send.encode())
    send=""
    for n in range(0,dim//4096):
        send+="04096"
        send+=os.read(fd,4096).decode()
        peer.send(send.encode())
        send=""
    if(last!=0):
        send+=Resize(str(last),5)
        send+=os.read(fd,4096).decode()
        peer.send(send.encode())
    os.close(fd)
    

    


def AvvioAscoltoServer(porta):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("",int(porta)))
    sock.listen(10)
    while True:
        client,addr= sock.accept()
        pid=os.fork()
        #pid=0
        if(pid==0):
            richiesta=client.recv(4).decode()
            if(richiesta=="RETR"):
                md5=client.recv(32).decode()
                for n in range(0,len(listaFileCondivisi)):
                    if(listaFileCondivisi[n][1]==md5 and Path(percorso+"/"+listaFileCondivisi[n][0]).is_file()==True and calcoloMD5(percorso+"/"+listaFileCondivisi[n][0])==md5):
                        InvioFile(client,percorso+"/"+listaFileCondivisi[n][0])
                        break
                client.send(("ARET"+"000000").encode())
            client.close()
            exit()
            

def DownloadFilePeer(ip,port,md5,namefile):
    send="RETR"+md5
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((ip,int(port)))
    except:
        print("il server non è raggiungibile, riprova più tardi")
        
        return
    client.send(send.encode())
    client.recv(4)
    pid=os.fork()
    if(pid==0):
        chunk=int(client.recv(6).decode())
        if(chunk==0):
            print("il file è vuoto oppure non è più in condivisione\n")
            exit()
        if(exists("download/"+namefile)): os.remove("download/"+namefile)
        fd = os.open("download/"+namefile, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o777)
        for n in range(0,chunk):
            buf=client.recv(int(client.recv(5).decode()))
            os.write(fd,buf)
        os.close(fd)
        print("ricevuto il file "+namefile)
        client2=SendData("RREG"+sessionid+md5+prepIp(ip)+Resize(str(port),5),ipDirectory,80)
        client2.recv(4)
        print(f"il file è stato scaricato {int(client2.recv(5).decode())} volte")
        client2.close()

        client.close()
        exit()

def RimuoviFile(sessionid,md5):
    send="DELF"+sessionid+md5
    client=SendData(send,ipDirectory,80)
    client.recv(4)
    totmd5=client.recv(3).decode()
    print(f"il file {list(filter(lambda x: x[1]==md5,listaFileCondivisi))[0][0]} è stato rimosso dalla condivisione\nCopie del file ancora in condivisione {totmd5}")


def AggiornaFileCondivisi(listaFileCondivisi,listaNuova):
    files = os.listdir(percorso)
    for n in files:
        listaNuova.append([n,calcoloMD5(percorso+"/"+n)])
    
    #rimozione file non più presenti
    for n in range(0,len(listaFileCondivisi)):
        tmp=list(filter(lambda x:x[1]==listaFileCondivisi[n][1],listaNuova))
        if(len(tmp)==0):
            RimuoviFile(sessionid,listaFileCondivisi[n][1])
            
    for n in range(0, len(listaNuova)):
        tmp=list(filter(lambda x:x[1]==listaNuova[n][1],listaFileCondivisi))
        if(len(tmp)==0):
            Aggiungi(sessionid,listaNuova[n][0])
    listaFileCondivisi=listaNuova.copy()
    return listaFileCondivisi.copy()
            
def Logout():
    send="LOGO"+sessionid
    client=SendData(send,ipDirectory,80)
    client.recv(4)
    nfile=client.recv(3).decode()
    print("Log out effettuato\nSono stati rimossi dalla condivisione "+nfile+" file")
    os.abort()
        
def Ctrl_c(signal,frame):
    Logout()
        
            


    





ipDirectory=str(sys.argv[1])
#ipDirectory="192.168.1.110"
sessionid, porta=Login(str(random.choice(range(49152,65536))))
if(sessionid=="0000000000000000"):
    print("Si è verificato un errore durante il processo di Log-in")
    exit()

print(f"Il tuo sessionID = {sessionid}")

signal.signal(signal.SIGINT, Ctrl_c)

server_client=threading.Thread(target=AvvioAscoltoServer,args=(porta,))
server_client.start()
listaFileCondivisi=[]
listaNuova=[]
percorso = "file_condivisi"



while True:
    scelta = input("Scegli azione da svolgere: \n1)Aggiorna file condivisi\n2)Ricerca file\n3)Ricevi file\n4)Logout\n")
    if(scelta == "1"):
        listaFileCondivisi=AggiornaFileCondivisi(listaFileCondivisi,listaNuova)
        listaNuova.clear()

    elif(scelta == "2"):
        daCercare = input("scegli il file da cercare\n")
        if(len(daCercare)<1 or len(daCercare)>20):
            print("contenuto non valido")
            continue
        Ricerca(sessionid,daCercare)

    elif(scelta == "3"):
        ipPeer=input("Inserisci l'ip del peer dal quale scaricare\n")
        portaPeer=input("Inserisci la porta del peer\n")
        md5Download=input("inserisci l'md5 del file da scaricare\n")
        namefile=input("nome con il quale salvare il file\n")
        DownloadFilePeer(ipPeer,portaPeer,md5Download,namefile)


    elif(scelta == "4"):
        Logout()
        
    else:
        print("Opzione non valida")


