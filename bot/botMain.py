# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 10:08:43 2017

@author: Charlotte
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup,ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
from student import Student 

TOKEN = "396513103:AAGL6bgtsy1jnpAxLbTe5HmPLDxCHY1MzxM"

# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

legalAnswersRegex =""
legalAnswers=[]

# somehow the pattern gets lost after each use. As a work around I set it agein
regEx_RegularChoice=RegexHandler(legalAnswersRegex,
                    regular_choice,
                    pass_user_data=True)

def start_course(bot,update, student, user_data):
    if student.course.attr["photo"] and student.course.attr["photo"] != "":
        img = open(student.course.attr["photo"], 'rb')
        update.message.reply_photo(photo=img)
        img.close()
    update.message.reply_text(student.course.attr["intro"].format(student.firstName))
    first_step=student.course.firstStep()
    student.step=first_step
    return play_step(update,student)

def continue_course(bot, update, student, user_data):
    text = update.message.text
    (next_step,same_course,command)=student.step.nextStep(text)
    if command:
        print 'command:',command
        return handle_command(bot, update, user_data, command)
       
    if next_step and same_course:
        student.step=next_step
        return play_step (update, student)
    elif next_step and not same_course:
        student.course.nextCourse()
        return start_course(bot, update, student, user_data)
    # tdb: go to next course
    return (None)

def exec_action(bot, update,student, user_data):
    text = update.message.text
    (action, args)=student.step.getAction(text)
    if action:
        if action=='student':
            student.exec_action(args)

def play_sequence(update, student, seq, markup=None):
    if seq["type"]=="text":
        text=seq["content"]
        update.message.reply_text(text.format(student.firstName),
                                  reply_markup=markup)
    elif seq["type"]=="photo":
        photo=open(seq["content"],'rb')
        update.message.reply_photo(photo=photo,
                                  reply_markup=markup)
        photo.close()
        
    elif seq["type"]=="video":
        video=open(seq["content"],'rb')
        update.message.reply_video(video=video,caption=seq['caption'],
                                  reply_markup=markup)
        video.close()
   
def play_step(update, student):
    step=student.step
    seq=step.attr["seq"]
    for i in range(len(seq)-1):
        play_sequence(update, student, seq[i], markup=None)
            
    if "answers" in step.attr:
        #multi-coice answer
        answers=step.attr["answers"]
        legalAnswers=answers.keys()

        #set RegEx
        #set regEx, i.e. ^(Age|Favourite colour|Number of siblings)$
        legalAnswersRegex="^({})$".format('|'.join(legalAnswers))
        regEx_RegularChoice.pattern=legalAnswersRegex

        #make keyboard
        stepMarkup=ReplyKeyboardMarkup([answers.keys()], 
                                        one_time_keyboard=True,
                                        resize_keyboard=True)
        play_sequence(update, student, seq[-1], markup=stepMarkup)
        
        return CHOOSING
  

def start(bot, update, user_data):
    student=Student(update )
    user_data['student']=student

    return start_course(bot,update, student, user_data)


def regular_choice(bot, update, user_data):
    student=user_data['student']
    exec_action(bot, update,student, user_data)
    return continue_course(bot, update, student, user_data)
    

def custom_choice(bot, update, user_data):
    markup=ReplyKeyboardRemove()
    student=user_data['student']
    update.message.reply_text('Da hast du mich falsch verstanden: du hast etwas eingetippt. '+
                              'Das war so nicht gewollt. Unterhalb der Eingabezeile gibt es '+
                              'Knöpfe, die du antippen sollst. Versuchs nochmal:', markup=markup)

    return play_step(update, student)

def custom_choice2(bot, update, user_data):
    print 'custom_choice2'
    return custom_choice(bot, update, user_data)

def custom_choice3(bot, update, user_data):
    print 'custom_choice3'
    return custom_choice(bot, update, user_data)
    
def handle_command(bot, update, user_data, command=None):
    if not command:
        command=update.message.text
    if command == '/cancel':
        update.message.reply_text('und Tschüss...')
        user_data.clear()
        return ConversationHandler.END
    elif command=='/start':
        return start (bot, update, user_data)
    elif command.startswith('/configError'):
        logger.error("{}".format(command))

    logger.info("unknown command {}".format(command))
    return start (bot, update, user_data)



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start,pass_user_data=True)],

        states={
            CHOOSING: [
                      regEx_RegularChoice,
                      RegexHandler('^/',
                                    handle_command,
                                    pass_user_data=True),
                      RegexHandler('^.',
                                    custom_choice,
                                    pass_user_data=True),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           custom_choice2,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^', custom_choice3, pass_user_data=True)],
        allow_reentry=True
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()