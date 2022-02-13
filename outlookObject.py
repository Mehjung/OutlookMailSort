from abc import ABC, abstractmethod
from cmath import e
import string
import os
import win32com.client

class outlookApi(object):

    def __init__(self) -> None:
        self.__mapi = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.olFolderInbox = 6
        self.olNameSpace = self.__mapi

    def printSubjectFromMailin(self, mailname):
        for x in self.getInboxItemsFromMailIn([mailname]):
            print (x.Subject)
        

    def getInboxItemsFromMailIn(self, mailInName):
        for x in mailInName:
            if self.__mailInExists(x):
                return self.__getInbox(self.__mapi.Folders(x)).items

    def __mailInExists(self, mailInName: string) -> bool:
        try:
            self.__mapi.Folders(mailInName)
            return True
        except BaseException as e:
            return not(e.args[0]==-2147352567)

    def __getInbox(self, object):
        try:
            return object.Folders("Posteingang")
        except BaseException as e:
            return object.Folders("Inbox")
   
    def p(self):
        for x in self.__mapi.folders:
            print(x.name)

    def find(self, id, mailInBox):
        return self.__mapi.GetItemFromID(id).Subject
    
ol = outlookApi()
#ol.p()
#ol.printSubjectFromMailin("Jan.Ehrmantraut@deutschebahn.com")
print(ol.find("00000000874D1B6A6D17A24AB78977D94C9943410700F97EE50A14DD0D40B89EC2D8805390DC00000000010C0000F97EE50A14DD0D40B89EC2D8805390DC00031CAEC6E20000","Jan.Ehrmantraut@deutschebahn.com"))