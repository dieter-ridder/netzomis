# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:05:14 2017

@author: Charlotte
"""
import time;
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from course import (Course, CourseStep)


class Student:
    def __init__(self, update):
        self.studentId = update.message.from_user.id
        self.firstName = update.message.from_user.first_name
        self.chatId=update.message.chat.id
        self.attr={}
        self.course=Course("newbie")
        self.step=self.course.firstStep()
        self.lastContact=update.message.date
        self.lastText=update.message.text
                
    def dump(self):
        text="\nfirstName: {}, studentId: {}, chatId: {}\n".format(\
            self.firstName, self.studentId, self.chatId)
        text+="os: {}, device: {}, mailAddress: {}\n".format(\
            self.os, self.device, self.mailAddress)
        text+=self.course.dump()
        text+=self.step.dump()
        text+="lastContact: {}\n".format(self.lastContact)
        text+="lastText:{}".format(self.lastText)
        return(text)
        
    def exec_action(self,args):
        if args[0]=='set':
            self.attr[args[1]]=args[2]
            
        
    def handleNewbie(self):
        answers=[]
        keyboard=None
        if self.step == 0:
            answers.append("Hallo {}, schön dich kennen zu lernen 😃!".format(self.firstName))
            self.step+=1

        #elif self.step == 1:
            answers.append("Bevor wir loslegen, möchte ich wissen, was für einen Gerätetyp du hast. Bitte wähle aus:")
            keyboard=[["iOS(Apple)","Android","keine Ahnung"]]
            self.step+=1
            
        elif self.step == 2:
            if self.lastText == "iOS(Apple)" or self.lastText == "Android":
                self.os=self.lastText
                answers.append("und was für ein Gerät?")
                if self.lastText == "iOS(Apple)":
                    keyboard=[["iPhone","iPad","iPad mit Mobilfunk"]]
                else:
                    keyboard=[["Smartphone", "Tablet", "Tablet mit Mobilfunk"]]
                self.step+=1
            else:
                answers.append("dann müssen wir zusammen nachsehen")
                self.step=10
                
        elif self.step == 3:
            self.device=self.lastText
            self.step=0
            self.course="Telegram"
            answers.append("Dann kann es ja losgehen, ok?")
            keyboard=[["weiter"]]

        else:
            self.step=0
            self.course="Telegram"
            answers.append("Dann kann es ja losgehen, ok?")
            keyboard=[["weiter"]]
            
        return (answers,keyboard)

            
        
    def handle(self, message):
        self.chatId=message["chat"]["id"]
        self.lastContact=message["date"]
        self.lastText=message["text"]
        
        #new student
        if self.course=="newbie":
            return (self.handleNewbie())
        
        return (["Hallo {}, schön dich wieder zu sehen".format(self.firstName)], None)




