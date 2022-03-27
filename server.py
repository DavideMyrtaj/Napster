import hashlib, sys, unittest

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
