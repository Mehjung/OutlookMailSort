from abc import ABC, abstractmethod
import os
import win32com.client

class outlookApi(object):

    def __init__(self) -> None:
        self.__mapi = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        
        

    def getMailInStoreByName(self, name ):
        pass

    def print(self):
        for x in self.__mapi.Folders:
            print (x.Name)


ol = outlookApi()
ol.print()

