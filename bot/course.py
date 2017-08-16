# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 10:27:58 2017

@author: Charlotte
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

courses={
         "newbie": {"photo": "./resources/newbie.jpg",
                    "intro": "Hallo {}, herzlich willkommen bei Netz-Omi. Ich helfe dir, "+
                             "dich mit deinem Smartphone, oder Tablet anzufreunden, und damit "+
                             "zu üben. Nach dem Kurs solltest du dich damit sicherer fühlen und "+
                             "damit einfach mit Freunden und Familie in Kontakt bleiben. \nWundere dich nicht, wenn ich "+
                             "etwas steif bin, ich bin nur ein Programm, und deshalb nicht sehr flexibel.",
                    "next": "desktop_1",
                    "prev": "",
                    "first_step":"newbie_1"
                    },
         "desktop_1": {"photo": "./resources/desktop_1.jpg",
                    "intro": "Jetzt zeige ich dir deinen Schreibtisch, den 'Desktop': Er ist der Dreh- und Angelpunkt, den dort liegen die 'APP's (Programme).",
                    "next": "ende",
                    "prev": "newbie",
                    "first_step":"desktop_1_1"
                    },
         "telegram_1": {"photo": "./resources/logo.jpg",
                    "intro": "Hallo {}, wir werden in dieser Lektion die App anschauen, "+
                             "in der du gerade bist. Sie heißt 'Telegram'. Das Logo siehst du oben."+
                             "Es sieht aus wie ein Papierflieger, auf blauem Grund. "+
                             "Telegram ermöglicht es, schnell und einfach kurze Texte, Bilder, Video zwischen Freunden "+
                             "austauschen. Bitte deine Familie, und deine Freunde, auch Telegram "+
                             "zu installieren.",
                    "next": "telegram_2",
                    "prev": "desktop_1",
                    "first_step":"telegram_1_1"
                    },
         "ende": {"photo": "",
                    "intro": "Herzlichen Glückwunsch! du bist am Ende des Kurses!",
                    "next": "newbie",
                    "prev": "desktop_1",
                    "first_step":"ende_1"
                    },
         }
         
courseStep={
            "newbie_1": {"seq":[{"type":"text", 
                                 "content": "Bevor wir loslegen, möchte ich noch von Dir wissen, "+
                                            "was für ein Gerät du hast. Bitte wähle unten zwischen "+
                                            "Smartphone oder Tablet aus:"}
                                ],
                         "actions":{"Smartphone":('student',['set','device', 'Smartphone']),
                                    "Tablet":('student',['set','device','Tablet'])},
                         "answers":{"Smartphone":"newbie_2",
                                    "Tablet":"newbie_2"},
                         "course":"newbie"
                        },
            "newbie_2": {"seq":[
                                {"type":"text",
                                 "content":"Danke, und jetzt will ich noch wissen, was für Software dort "+
                                           "dort installiert ist: Android, iOS(Apple), windows. "+
                                            "Bitte wähle wieder aus:"}
                                ],
                         "actions":{"Android":('student',['set','os', 'Android']),
                                    "iOS":('student',['set','os', 'iOS'])},
                         "answers":{"Android":"newbie_3",
                                    "iOS":"newbie_3",
                                    "windows":"newbie_4",
                                    "keine Ahnung":"newbie_5"},
                         "course":"newbie"
                         },
            "newbie_3": {"seq":[{"type":"text", 
                                 "content": "Danke, dann können wir jetzt anfangen. "+
                                            "Wenn du soweit bist, tippe unten auf 'weiter'"}
                                ],
                         "answers":{"weiter":"telegram_1_1"},
                         "course":"newbie"
                        },
                        
            "newbie_4": {"seq":[{"type":"text", 
                                 "content": "Du hast ein Smartphone oder Tablet mit windows? Das ist "+
                                            "aber schade, denn auf windows bin ich noch nicht "+
                                            "eingestellt. Wenn du dich allerdings schon etwas "+
                                            "auskennst, dann kannst du es trotzdem versuchen. "+
                                            "Vieles in den Apps ist ähnlich, und Du lernst trotzdem etwas"}
                                ],
                         "actions":{"weiter":('student',['set','os', 'Android'])},
                         "answers":{"weiter":"newbie_3",
                                    "Abbruch":"/cancel"},
                         "course":"newbie"
                        },
                        
            "newbie_5": {"seq":[
                                {"type":"text",
                                 "content":"Am einfachsten bekommst du das heraus, wenn du die  "+
                                           "Taste mitten auf dem Rahmen drückst. Damit kommst du "+
                                            "zu deinem Schreibtisch, und schaust dir das Symbol an, "+
                                            "mit dem du diese App aufgerufen hast. Das war der "+
                                            "weiße Papierflieger auf blauem Grund"},
                                {"type":"photo",
                                 "content":"./resources/Apple_oder_Android.png"},
                                {"type":"text",
                                 "content":"Papierflieger in blauen Kreis: Android, in blauen Kreis in "+
                                           "einem Quadrat mit abgerundeten Ecken: Apple - Wenn er ein bischen komisch "+
                                            "aussieht und der Desktop aus großen 'Kacheln' besteht: Windows "+
                                            "Also: zum Schreibtisch, die Form merken, wieder drauf tippen, und "+
                                            "unten auswählen"},
                                ],
                         "actions":{"Android":('student',['set','os', 'Android']),
                                    "iOS(Apple)":('student',['set','os', 'iOS(Apple)'])},
                         "answers":{"Android":"newbie_3",
                                    "iOS(Apple)":"newbie_3",
                                    "windows":"newbie_4",
                                    "Abbruch":"/cancel"},
                         "course":"newbie"
                         },
                         
            "desktop_1_1": {"seq":[{"type":"text",
                                     "content": "Im Rahmen ist der 'HOME'-Knopf, mit dem du aus jeder APP wieder auf "+
                                                "den Desktop kommst. Die vielen bunten Bildchen dort, "+
                                                "das sind 'APP's, d.h. Programme. Du bist gerade in so einer APP. Wenn du auf 'HOME' tippst, "+
                                                "kommst du auf den Desktop, wenn du dort auf den blauen Kreis mit Papierflieger tippst,  "+
                                                "kommst du wieder zurück. Das Video zeigt dir das schematisch. Um es zu starten, und später zu stoppen, "+
                                                "musst du es antippen"},
                                   {"type":"video",
                                    "content":"./resources/desktop_1.mp4",
                                    "caption":"zum Desktop und zurück in die App"},
                                    {"type":"text",
                                     "content": "Fertig mit dem Video? Bitte noch NICHT ausprobieren! Tippe unten auf 'weiter', "+
                                                "dann verrate ich dir auch, warum."}
                                    ],
                         "answers":{"weiter":"desktop_1_2"},
                         "course":"desktop_1"
                        },
                        
            "desktop_1_2": {"seq":[
                                    {"type":"text",
                                     "content": "Es ist möglich, dass du auf dem DESTKOP das Symbol mit dem Papierflieger nicht siehst. "+
                                                "Dann ist er auf einer anderen Seite des DESKTOPs. Stell es dir so vor: " +
                                                "Der DESKTOP ist ein langes Band, und das Gerät ist wie ein Fenster, durch das du "+
                                                "einen Ausschnitt siehtst. Durch Wischen mit dem Finger von links nach rechts "+
                                                "kannst den Ausschnitt, den du siehst, verschieben. Das Video versucht, es zu erklären:"},
                                   {"type":"video",
                                    "content":"./resources/desktop_2.mp4",
                                    "caption":"Desktop: verschiedene Seiten"},
                                    {"type":"text",
                                     "content": "Fertig mit dem Video? JETZT ausprobiere es aus!"},
                                     {"type":"text",
                                     "content": "Wenn du vom DESKTOP zurück bist, tippe unten auf 'weiter':"}
                                    ],
                         "answers":{"weiter":"ende_1"},
                         "course":"desktop_1"
                        },
                        
            "telegram_1_1": {"seq":[{"type":"text", 
                                     "content": "Als erstes müssen wir sicher sein, dass du immer "+
                                            "wieder zu mir zurück kommst. Das probieren wir jetzt als erstes"
                                    },
                                    {"type":"text",
                                     "content": "Auf dem Rande deines Geräts ist ein Knopf, mit dem du auf "+
                                                "auf deinen Schreibttisch kommst. Dort liegen viele bunte Bildchen, "+
                                                "das sind alles Programme, neudeutsch 'Apps'. Wenn man drauftippt, "+
                                                "ruft man sie auf. Um hierhin zurückzukommen, musst "+
                                                "auf das blaue Symbol mit Papierflieger tippen"},
                                    {"type":"text",
                                     "content": "Es ist möglich, dass du den Papierflieger nicht siehst. "+
                                                "Dann ist er auf einer anderen Seite des Schreibtisch. " +
                                                "Dein Schreibtisch ist größer als der Bildschirm, deshalb "+
                                                "siehst du immer nur einen Teil. Durch Wischen mit dem Finger von links nach rechts "+
                                                "kannst den Ausschnitt, den du siehst verschieben. Ich hoffe, meine Zeichnung machts das klar "+
                                                "Probiere es jetzt aus. Wenn du wieder zurück bist, tippe unten auf 'weiter'" }
                                    ],
                         "answers":{"weiter":"telegram_1_1"},
                         "course":"telegram_1"
                        },
            "ende_1": {"seq":[
                                {"type":"text",
                                 "content":"Hoffentlich hat es Dir Spaß gemacht, und wir sehen dich bei "+
                                           "einem anderen Kurs wieder."},
                                ],
                         "answers":{"ENDE":"/cancel",
                                    "Nochmal von vorn":"/start"},
                         "course":"ende"
                         },
                         
            }

class Course:
    def __init__(self, name):
        self.name=name
        self.attr=courses[self.name]

    def dump (self):
        return ("course: {}, photo: {} \n1st step: {}, prev: {}, next: {}, \nintro: {}\n".format(\
              self.name,self.attr["photo"],\
              self.attr["first_step"], self.attr["prev"], self.attr["next"],\
              self.attr["intro"]))
        
    def firstStep(self):
        step=CourseStep(self.attr["first_step"])
        return(step)
        
    def nextCourse(self):
        if not "next" in self.attr:
            return None
        
        nextCourse=self.attr["next"]
        if not nextCourse in courses:
            return None
            
        self.name=nextCourse
        self.attr=courses[self.name]
        
        
class CourseStep:
    def __init__(self, name):
        
        self.name=name
        self.attr=courseStep[self.name]

    def dump (self):
        text="step: {} - seq:\n".format(self.name)
        for s in self.attr["seq"]:
              text+="type: {}, content: {}\n".format(s["type"],s["content"]) 
        text+="legal answers: {}\n".format(self.attr["answers"])
        return (text)
        
    def nextStep(self, text):
        (nextStep,sameCourse,command)=(None,False,None)
        #is there a next step defined?
        print text
        if text.startswith('/'):
            command=text
            return (nextStep,sameCourse,command)
            
        if 'answers' in self.attr and text in self.attr['answers']:
            nextName=self.attr['answers'][text]
        else:
            command="/configError: no next step for {}, {}".format(self.name, text)
            return (nextStep,sameCourse,command)           # no next step defined
            
        #if it a command?
        if nextName.startswith('/'):
            command=nextName
            return (nextStep,sameCourse,command)

        #does next step exist and belongs to same course?
        
        if not nextName in courseStep:
            command="/configError: nextstep {} not defined".format(nextName)
            return None          # no step found

        #does next step belong to the same course?
        recentCourse=self.attr['course']
        sameCourse=False
        if courseStep[nextName]['course']==recentCourse:
            sameCourse=True
        return(CourseStep(nextName), sameCourse, None)
        
    def getAction(self, text):
        (action, args)=(None, None)
        if 'actions' in self.attr and text in self.attr['actions']:
            (action, args)=self.attr['actions'][text]
        return (action, args)
                
