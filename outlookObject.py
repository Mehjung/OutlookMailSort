from abc import ABC, abstractmethod
from cmath import e
import string
import os
import win32com.client

class outlookApi(object):
    """
    Outlook Api Wrapper:
    """

    def __init__(self) -> None:
        self.__mapi = self.outlookObject().GetNamespace("MAPI")

    def printSubjectFromMailin(self, *mailname):
        ''' Gibt den EMail Subject Titel der Emails aus dem Posteingang des Arguments auf der Console aus.'''
        box = self.getInboxItemsFromMailIn(*mailname)
        if box is not None:
            for x in box:
                print (x.Subject)
        else:
            print ("No MailBox to print out!")

    def getInboxItemsFromMailIn(self, *mailInName):
        ''' Gibt die Items aus dem Posteingang des Arguments zurück.'''
        for box in mailInName:
            if self.__mapi.FolderExists(box):
                return self.__mapi.Folders(box).Folders("Posteingang").items

    def find(self, id, mailInBox):
        ''' gibt ein Item Object basieren auf der Angabe der ID zurueck.'''
        return self.__mapi.GetItemFromID(id)
    
    class outlookObject(object):
        
        def __init__(self) -> None:
            self.__outlook = win32com.client.Dispatch("Outlook.Application")
            self.__aliase = {"Posteingang":"Inbox", "Inbox":"Posteingang"}
        
        def Folders(self , name):
            if self.FolderExists(name):
                self.__outlook = self.__outlook.Folders(name)
            elif self.__tryAliasFolder(name):
                self.__outlook = self.__outlook.Folders(self.__aliase[name])
            else:
                print ("Folder " + name + " not found!")
            return self
       
        def __tryAliasFolder(self, name):
            return name in self.__aliase and self.FolderExists(self.__aliase[name])
                

        def GetNamespace(self, mapi):
            self.__outlook = self.__outlook.GetNamespace(mapi)
            return self

        def FolderExists(self, mailInName: string) -> bool:
            try:
                self.__outlook.Folders(mailInName)
                return True
            except BaseException as e:
                return not(e.args[0]==-2147352567)
        
        def __getattr__(self, name):
            try:
                return getattr(self.__outlook, name)
            except AttributeError:
                raise AttributeError(
                    "'%s' object has no attribute '%s'" % (type(self).__name__, name))




ol = outlookApi()
#ol.p()
ol.printSubjectFromMailin("Jan.Ehrmantraut@deutschebahn.com")
#print(ol.find("00000000874D1B6A6D17A24AB78977D94C9943410700F97EE50A14DD0D40B89EC2D8805390DC00000000010C0000F97EE50A14DD0D40B89EC2D8805390DC00031CAEC6E20000","Jan.Ehrmantraut@deutschebahn.com"))






