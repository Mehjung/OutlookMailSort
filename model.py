from abc import ABC, abstractmethod
from xmlRulesReader import *
from outlookObject import *
from pprint import pprint
import time
import logging

class mailSystem(dict):

    def move(self, mailID, dest, *args):
        self[mailID] = ('MOVE', dest)

    def delete(self, mailID, *args):
        self[mailID] = ('DELETE',)

    def read(self, *args):
        cnt = args[2]
        if not("READER_ID" in self):
            self["READER_ID"] =('READ', cnt, )

def matchActions(createDASLString, olAPI, system, ruleSets):

    def matchRule(mail, rule, cnt):
        getattr(system, rule.operation) (mail.EntryID, olAPI.getFolderByString(rule.targetPath), cnt)

    def syncRulesToMailItems(rules):
        for rule in rules:
            mailItems = getMailsByFilter(rule.criteria)
            cntItems = len(list(getMailsByFilter(rule.criteria)))
            for ml in mailItems:
                matchRule(ml,rule , cntItems)

    def getMailsByFilter(criteria):
        return olAPI.readMailItemsFromInboxByFilter(createDASLString, criteria)

    for ruleset in ruleSets:
        recipient = ruleset.Recipient
        olAPI.setRecipient(recipient)
        rules = ruleset.rules
        syncRulesToMailItems(rules)

def executeActions(system, ol, logger):
    getMailObject = ol.find

    for id, (action, *args) in system.items():
        #print(id + " -> " + action)

        if action == 'DELETE':
            #print (getMailObject(id).Subject + " wurde gelöscht.")
            logger.logDel(getMailObject(id))
        if action == 'MOVE':
            #print (getMailObject(id).Subject + " wurde nach " + args[0].FullFolderPath + " verschoben.")
            logger.logMove(getMailObject(id), args[0].FullFolderPath)
        if action == 'READ':
            #print ("Es wurden " + str(args[0]) + " Elemente gezählt.")
            logger.logRead(args[0])

class logger():

    def __init__(self) -> None:
        
        self.logDict = { 
                        'move'      : logging.getLogger('move'),
                        'delete'    : logging.getLogger('delete'),
                        'read'      : logging.getLogger('read')
        }
        
        for lg, lgObj in self.logDict.items():
            lgObj.setLevel(logging.INFO)
            
            file_handler = logging.FileHandler(lg + '.log', mode = 'w', encoding = 'utf-8')
            file_handler.setLevel(logging.INFO)
            
            #formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' + \
            #                              '(%(filename)s:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S')
            
            #file_handler.setFormatter(formatter)
            lgObj.addHandler(file_handler)
    
    def logDel(self, olObj):
        _logger = self.logDict['delete']
        self.commonLogging(olObj, _logger)
        _logger.info("\n\n")

    def logMove(self, olObj, path):
        _logger = self.logDict['move']
        self.commonLogging(olObj, _logger)
        _logger.info("Path:      " + path + "\n\n")

    def logRead(self, cnt):
        _logger = self.logDict['read']
        _logger.info("Mails read:    " + str(cnt)+ "\n\n")
        

    def commonLogging(self, olObj, _logger):
        if olObj.SenderEmailType == "EX":
            sender = olObj.Sender.GetExchangeUser().PrimarySmtpAddress
        else:
            sender = olObj.SenderEmailAddress
        _logger.info(
                    "Subject:   " + olObj.Subject + "\n" \
                    "Date:      " + str(olObj.ReceivedTime) + "\n" \
                    "Sender:    " + sender + "\n" \
                    "Mail Type: " + olObj.SenderEmailType 
                    )
  

xmlFile = 'rules.xml'
xml = xmlReader(xmlFile)
xmlFuncTest = xmlReaderMethods(xml.root)
rules = xmlFuncTest.getRuleSets()
system = mailSystem()

start = time.time()

matchActions(filter, outlookApi(), system, rules)
executeActions(system, outlookApi(), logger())

end = time.time()
print ( end - start)
