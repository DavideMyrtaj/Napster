import hashlib, sys, unittest,socket
from syslog import LOG_INFO
from os import fork

from soupsieve import match

class Server:
    @staticmethod
    def Login(ip, porta):

        print("Login: ")

    @staticmethod
    def CercaPeer(sessionID):
        print("Inserisci il sessionID del peer ricercato")

    @staticmethod
    def Aggiungi(sessionID, md5, descrizione):
        print("Inserisci il file da aggiungere")

    @staticmethod
    def Delete(sessionID, md5):
        print("Inserisci il sessionID da eliminare")

    @staticmethod
    def Ricerca(sessionID, testo):
        print("Inserisci il file da cercare")

    @staticmethod
    def Logout(sessionID):
        print("Logout")

    @staticmethod
    def RegistraDownload(md5, sessionID):
        print("Registra Download")

    
    def Parser(pacchetto):

        if(pacchetto=="LOGI"):
            ip=client.recv(15).decode()
            porta=client.recv(5).decode()
            Server.Login(ip,porta)
        elif(pacchetto=="ADDF"):
            sessionId=client.recv(16).decode()
            md5=client.recv(32).decode()
            filename=client.recv(100).decode()
        elif(pacchetto=="DELF"):
            sessionId=client.recv(16).decode()
            md5=client.recv(32).decode()
        elif(pacchetto=="FIND"):
            sessionId=client.recv(16).decode()
            ricerca=client.recv(20).decode()

    
    

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("",50000))

sock.listen(50)

while True:
    print("server in ascolto....\n")
    client,addr= sock.accept()
    pid=0
    if(pid==0):
        richiesta=client.recv(4).decode()
        Server.Parser(richiesta)
        client.close()
        exit()








