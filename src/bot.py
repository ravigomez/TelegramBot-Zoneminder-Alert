import os
<<<<<<< HEAD
import logging
import subprocess
import time

from os.path import join, dirname
from dotenv import load_dotenv

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tinydb import TinyDB, Query, where

from ZoneMinderDB import ZoneMinderDB
from ZoneMinderScraper import ZoneMinderScraper

db = TinyDB('localDB/db.json')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

dotenv_path = join(dirname(__file__), '..', '.env')

load_dotenv(dotenv_path)


def __isTheOwner(update):
    if update.message.from_user.name.lower() == os.environ.get('TELEGRAM_OWNER_NAME').lower():
        return True
    else:
        return False


def __allowedUser(update):
    if __isTheOwner(update):
        return True
    else:
        current_user = update.message.from_user.name.lower()
        table = db.table('AllowedUsers')
        user = table.get(Query().telegram_name == current_user)
        if user is not None:
            return True
        else:
            return False


def start(update, context):
    if __allowedUser(update):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Hello {update.message.from_user.first_name} I\'m you bot. What can I do for you?")
    else:
        update.message.reply_text(
            f'You don\'t have permission to use this Bot.')


def main():
=======
from os.path import join, dirname
import logging

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from service.ZoneMinderService import ZoneMinderService
from service.NetworkService import NetworkService
from service.VideoService import VideoService
from service.UserService import UserService

UService = UserService()
ZMService = ZoneMinderService()
NService = NetworkService()
VService = VideoService()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

def main():        
>>>>>>> 675e88a9fe0f94d9703c4bbb91478c7cc6f777fe
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=os.environ.get(
        'TELEGRAM_BOT_API'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("adduser", addUser))
    dp.add_handler(CommandHandler("removeuser", removeUser))
<<<<<<< HEAD
    dp.add_handler(CommandHandler("latest", latest))
    dp.add_handler(CommandHandler("help", help_command))
=======
    dp.add_handler(CommandHandler("listusers", listUsers))
    dp.add_handler(CommandHandler("latest", latest))
    dp.add_handler(CommandHandler("getevent", getEvent))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("getip", getPublicIP))
    #dp.add_handler(CommandHandler("test", test))
>>>>>>> 675e88a9fe0f94d9703c4bbb91478c7cc6f777fe

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

<<<<<<< HEAD

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def addUser(update, context):
    reply = ''
    if __isTheOwner(update):
        new_user = update.message.text.replace('/adduser', '').strip().lower()
        if new_user != '':
            table = db.table('AllowedUsers')
            table.insert({'telegram_name': new_user})
=======
def start(update, context):
    if UService.isAllowedUser(update):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Hello {update.message.from_user.first_name} I\'m your bot. What can I do for you?")
    else:
        update.message.reply_text(
            f'You don\'t have permission to use this Bot.')

def help_command(update, context):
    update.message.reply_text('<-<-<- Help Menu ->->->')
    listCommands(update)

def addUser(update, context):
    if UService.isTheOwner(update):
        new_user_name = update.message.text.replace('/adduser', '').strip().lower()
        if new_user_name != '':
            UService.addUser(new_user_name)
>>>>>>> 675e88a9fe0f94d9703c4bbb91478c7cc6f777fe
            reply = 'user added!'
        else:
            reply = 'You need to specify a telegram name including @.'
    else:
        reply = 'You don\'t have permission. Only the owner can add new users.'
<<<<<<< HEAD

    update.message.reply_text(reply)


def removeUser(update, context):
    reply = ''
    if __isTheOwner(update):
        typed_user = update.message.text.replace(
            '/removeuser', '').strip().lower()
        if typed_user != '':
            table = db.table('AllowedUsers')
            user = table.get(Query().telegram_name == typed_user)
            table.remove(doc_ids=[user.doc_id])
=======
    
    if reply:
        update.message.reply_text(reply)

def removeUser(update, context):
    if UService.isTheOwner(update):
        typed_user = update.message.text.replace(
            '/removeuser', '').strip().lower()
        if typed_user != '':
            UService.removeUser(typed_user)
>>>>>>> 675e88a9fe0f94d9703c4bbb91478c7cc6f777fe
            reply = 'user removed!'
        else:
            reply = 'You need to spcify a telegram name including @.'
    else:
        reply = 'You don\'t have permission. Only the owner can add new users.'

<<<<<<< HEAD
    update.message.reply_text(reply)


def latest(update, context):
    if not __allowedUser(update):
=======
    if reply:
        update.message.reply_text(reply)

def listUsers(update, context):
    if UService.isTheOwner(update):
        users = UService.listUsers()
        update.message.reply_text(users)
    else:
        reply = 'You don\'t have permission. Only the owner can add new users.'
        update.message.reply_text(reply)

def getPublicIP(update, context):
    if UService.isTheOwner(update):
        update.message.reply_text('Getting Public IP...')
        try:
            ns = NetworkService()
            ip = ns.getPublicIP()
            update.message.reply_text(f'Your Public IP is: {ip}')
        except:
            update.message.reply_text('ERROR while trying to get Public IP')
    else:
        update.message.reply_text(f'You don\'t have permission to use this Bot.')
        return

    listCommands(update)

def listCommands(update):
    if UService.isTheOwner(update):
        update.message.reply_text('Commands Available')
        update.message.reply_text('/getip')
        update.message.reply_text('/latest')
        update.message.reply_text('/removeuser')
        update.message.reply_text('/adduser')
        update.message.reply_text('/listusers')
        update.message.reply_text('/test')
    else:
        update.message.reply_text('Commands Available')
        update.message.reply_text('/latest')
        update.message.reply_text('/getevent')

def latest(update, context):
    if not UService.isAllowedUser(update):
>>>>>>> 675e88a9fe0f94d9703c4bbb91478c7cc6f777fe
        update.message.reply_text(
            f'You don\'t have permission to use this Bot.')
        return

<<<<<<< HEAD
    table = db.table('Config')

    if len(table.all()) == 0:
        latesteEventID = os.environ.get('ZONEMINDER_EVENT_ID_INITIAL')
    else:
        latesteEventID = table.all()[0]['EventID']

    update.message.reply_text('Reading events...')
    events = ZoneMinderDB().latestEvents(latesteEventID)

    update.message.reply_text(f'The bot is processing {len(events)} videos...')

    if len(events) > 0:
        ZoneMinderScraper().processVideos(events)

        for id in events:
            subprocess.call(
                f'ffmpeg -y -i src/Downloads/Event-_{id}-r4-s1.avi -strict -2 src/videos/{id}.mp4', shell=True)

        erro = False
        for id in events:
            try:
                context.bot.send_video(update.message.chat_id,
                                       video=open(f'src/videos/{id}.mp4', 'rb'), timeout=240)

            except:
                update.message.reply_text(
                    f'Erro while try to send video id: {id}')
                print(f'Erro while try to send video id: {id}')
                erro = True

        if not erro:
            update.message.reply_text('You have all the videos.')

            latesteEventID = events[len(events) - 1]

            if len(table.all()) > 0:
                table.update({'EventID': latesteEventID})
            else:
                table.insert({'EventID': latesteEventID})

        for id in events:
            if os.path.exists(f'src/Downloads/Event-_{id}-r4-s1.avi'):
                os.remove(f'src/Downloads/Event-_{id}-r4-s1.avi')
            if os.path.exists(f'src/videos/{id}.mp4'):
                os.remove(f'src/videos/{id}.mp4')

=======
    update.message.reply_text('Start to reading events...')
    user_name = update.message.from_user.name.lower()
    events = ZMService.getLatestEventsIDs(user_name, not UService.isTheOwner(update))

    if len(events) == 0:
        update.message.reply_text(f'There is no new videos to read...')
        return
    
    update.message.reply_text(f'Start to processing {len(events)} videos...')
    
    videoGenerateErrorCount = 0
    sendVideoErrorCount = 0
    for event in reversed(events):
        try:
            videoPath = VService.videoGenerate(event)
        except Exception as ex:
            update.message.reply_text(f'Error while generating a video of the event.')
            update.message.reply_text(f'ERROR: {ex}')
            update.message.reply_text(f'To try again use:')
            update.message.reply_text(f'/getevent {event}')
            videoGenerateErrorCount += 1
            continue
        
        try:
            context.bot.send_video(update.message.chat_id,
                                       video=open(videoPath, 'rb'), timeout=240)
        except Exception as ex:
            update.message.reply_text(f'Error while sending the video of the event. To try again use:')
            update.message.reply_text(f'ERROR: {ex}')
            update.message.reply_text(f'/getevent {event}')
            sendVideoErrorCount += 1
            continue
        
        VService.removeVideoFile(videoPath)
    
    if videoGenerateErrorCount == len(events) or sendVideoErrorCount == len(events):
        update.message.reply_text('All videos with error. Try Again.')
    else:
        ZMService.saveLatestEventID(user_name, events[0])
        update.message.reply_text('DONE You have all the videos.')
    
    listCommands(update)

def getEvent(update, context):
    if not UService.isAllowedUser(update):
        update.message.reply_text(
            f'You don\'t have permission to use this Bot.')
        return

    eventID = int(update.message.text.replace('/getevent', '').strip())

    update.message.reply_text('Getting this event...')

    if eventID <= 0:
        update.message.reply_text(f'EventID is invalid.')
        return
    
    update.message.reply_text(f'Start to processing the video...')

    try:
        videoPath = VService.videoGenerate(eventID)
    except Exception as ex:
        update.message.reply_text(f'Error while generating a video of the event number: {eventID}')
        update.message.reply_text(f'ERROR: {ex}')
        return
    
    try:
        context.bot.send_video(update.message.chat_id,
                                    video=open(videoPath, 'rb'), timeout=240)
    except:
        update.message.reply_text(f'ERROR while sending the video of the event number: {eventID}')
        return
    
    VService.removeVideoFile(videoPath)
    update.message.reply_text('DONE You have the videos.')    
    listCommands(update)
>>>>>>> 675e88a9fe0f94d9703c4bbb91478c7cc6f777fe

if __name__ == '__main__':
    main()
