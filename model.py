from abc import ABC, abstractmethod
from xmlRulesReader import *
from outlookObject import *
from pprint import pprint
import time

class mailSystem(dict):

    def move(self, mailID, dest, *args):
        self[mailID] = ('MOVE', dest)

    def delete(self, mailID, *args):
        self[mailID] = ('DELETE',)

    def read(self, *args):
        if not(args[2] in self):
            self["READ"] =('READ', args[2], )

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

def executeActions(system, ol):
    getMailObject = ol.find

    for id, (action, *args) in system.items():
        #print(id + " -> " + action)

        if action == 'DELETE':
            print (getMailObject(id).Subject + " wurde gelöscht.")
        if action == 'MOVE':
            print (getMailObject(id).Subject + " wurde nach " + args[0].FullFolderPath + " verschoben.")
        if action == 'READ':
            print ("Es wurden " + str(args[0]) + " Elemente gezählt.")

xmlFile = 'rules.xml'
xml = xmlReader(xmlFile)
xmlFuncTest = xmlReaderMethods(xml.root)
rules = xmlFuncTest.getRuleSets()
system = mailSystem()

start = time.time()

matchActions(filter, outlookApi(), system, rules)
executeActions(system, outlookApi())

end = time.time()
print ( end - start)
