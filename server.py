import hashlib, sys, unittest,socket, mysql.connector
from xmlrpc.client import SERVER_ERROR
from syslog import LOG_INFO
import random
import string
from os import fork


class Server:
    
    @staticmethod
    def SendData(send):
        client.send(str(send).encode())

    @staticmethod
    #aggiunge n 0 prima della stringa data come parametro fino ad avere una lunghezza uguale a dim
    def Resize(stringa, dim):
        tmp=""
        for n in range(0,dim-len(stringa)):
            tmp+="0"
        tmp+=stringa
        return tmp

    @staticmethod
    def session_generator(size=16, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    @staticmethod
    def Login(ip, porta):
        try:
            _sessionid=Server.session_generator()
            val=(_sessionid,ip,porta)
            mycursor.execute("INSERT INTO PEER (SESSION_ID, IP, PORTA) VALUES (%s,%s,%s)",val)
            mydb.commit()
                
        except mysql.connector.Error as err:
            _sessionid="0000000000000000"
        Server.SendData("ALGI"+_sessionid)

    @staticmethod
    def CercaPeer(sessionID):
        print("Inserisci il sessionID del peer ricercato")

    @staticmethod
    def Aggiungi(sessionID, md5, descrizione):
        try:
            val=(md5,descrizione,descrizione)
            mycursor.execute("INSERT INTO FILE (MD5,DESCRIZIONE) VALUES (%s,%s) ON DUPLICATE KEY UPDATE DESCRIZIONE=%s",val)
            mydb.commit()
            val=(md5,sessionID)
            mycursor.execute("INSERT INTO FILE_PEER (MD5,SESSION_ID) VALUES (%s,%s)",val)
            mydb.commit()
            print("peer aggiunto per la condivisione del file "+md5)
            
        except mysql.connector.Error as err:
            print("si è verificato il seguente errore "+ err.msg)

        val=(md5,)
        mycursor.execute("SELECT COUNT(SESSION_ID) FROM FILE_PEER WHERE MD5=%s",val)
        count=mycursor.fetchall()
        count=Server.Resize(str(count[0][0]),3)
        Server.SendData("AADD"+count)
        

    @staticmethod
    def Delete(sessionID, md5):
        val=(sessionID,md5)
        mycursor.execute("DELETE FROM FILE_PEER WHERE SESSION_ID=%s AND MD5=%s",val)
        mydb.commit()
        mycursor.execute(f"SELECT COUNT(*) FROM FILE_PEER WHERE MD5='{md5}'")
        count=mycursor.fetchall()[0][0]
        if(int(count)==0):
            mycursor.execute(f"DELETE FROM FILE WHERE MD5='{md5}'")
            mydb.commit()

        count=Server.Resize(str(count),3)
        Server.SendData("ADEL"+count)
        

    @staticmethod
    def Ricerca(sessionID, descrizione):
         #ordina per file con più download
        
        mycursor.execute(f"SELECT f.MD5, f.DESCRIZIONE, COUNT(f.MD5) AS TOT FROM FILE f INNER JOIN FILE_PEER fp ON fp.MD5=f.MD5 WHERE f.DESCRIZIONE LIKE '%{descrizione}%' GROUP BY (f.MD5) ORDER BY (TOT) DESC ")
        listmd5=mycursor.fetchall()
        send="AFIN"+Server.Resize(str(len(listmd5)),3)
        if(len(listmd5)==0):
            Server.SendData(send)
            return
        for n in range(0,len(listmd5)):
            send+=f"{listmd5[n][0]}{listmd5[n][1]}{Server.Resize(str(listmd5[n][2]),3)}"
           
            mycursor.execute(f"SELECT p.IP, p.PORTA FROM FILE_PEER fp INNER JOIN PEER p ON p.SESSION_ID = fp.SESSION_ID WHERE fp.MD5='{listmd5[n][0]}'")
            listapeer=mycursor.fetchall()
            for i in range(0,len(listapeer)):
                send+=f"{listapeer[i][0]}{listapeer[i][1]}"

        Server.SendData(send)
        



    @staticmethod
    def Logout(sessionID):
        send="ALGO"
        mycursor.execute(f"SELECT COUNT(*) FROM FILE_PEER WHERE SESSION_ID='{sessionID}'")
        filecondivisi=(mycursor.fetchall())[0][0]
        send+=Server.Resize(str(filecondivisi),3)
        mycursor.execute(f"DELETE FROM PEER WHERE SESSION_ID='{sessionID}'")
        mydb.commit()
        Server.SendData(send)
        

    @staticmethod
    def RegistraDownload(sessionid,md5,ipdown,portdown):
        val=(sessionid,md5,ipdown,portdown)
        mycursor.execute("INSERT INTO DOWNLOAD (SESSION_ID,MD5,IP,PORT) VALUES (%s,%s,%s,%s)",val)
        mydb.commit()
        mycursor.execute(f"SELECT COUNT(*) FROM DOWNLOAD WHERE MD5='{md5}'")
        totdownload=list(mycursor.fetchall())[0][0]
        send="ARRE"+Server.Resize(str(totdownload),5)
        Server.SendData(send)

    @staticmethod
    def Parser(pacchetto):

        try:

            if(pacchetto=="LOGI"):
                ip=client.recv(15).decode()
                porta=client.recv(5).decode()
                Server.Login(ip,porta)
            elif(pacchetto=="ADDF"):
                sessionId=client.recv(16).decode()
                md5=client.recv(32).decode()
                filename=client.recv(100).decode()
                Server.Aggiungi(sessionId,md5,filename)
            elif(pacchetto=="DELF"):
                sessionId=client.recv(16).decode()
                md5=client.recv(32).decode()
                Server.Delete(sessionId,md5)
            elif(pacchetto=="FIND"):
                sessionId=client.recv(16).decode()
                descrizione=client.recv(20).decode()
                Server.Ricerca(sessionId, descrizione)
            elif(pacchetto=="LOGO"):
                sessionId=client.recv(16).decode()
                Server.Logout(sessionId)
            elif(pacchetto=="RREG"):
                sessionId=client.recv(16).decode()
                md5=client.recv(32).decode()
                ipdown=client.recv(15).decode()
                portdown=client.recv(5).decode()
                Server.RegistraDownload(sessionId,md5,ipdown,portdown)
        except socket.socket.error as err:
            print(err)


    
    
mydb=0
mycursor = 0
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("",80))

sock.listen(50)

while True:
    print("server in ascolto....\n")
    client,addr= sock.accept()
    pid=fork()
    if(pid==0):
        mydb = mysql.connector.connect(host="localhost",user="root",password="123",database="DIRECTORY")
        mycursor = mydb.cursor()
        richiesta=client.recv(4).decode()
        Server.Parser(richiesta)
        client.close()
        exit()
        








