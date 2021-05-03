import os
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
    dp.add_handler(CommandHandler("listusers", listUsers))
    dp.add_handler(CommandHandler("latest", latest))
    dp.add_handler(CommandHandler("getevent", getEvent))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("getip", getPublicIP))
    #dp.add_handler(CommandHandler("test", test))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def start(update, context):
    if UService.isAllowedUser(update):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Hello {update.message.from_user.first_name} I\'m you bot. What can I do for you?")
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
            reply = 'user added!'
        else:
            reply = 'You need to specify a telegram name including @.'
    else:
        reply = 'You don\'t have permission. Only the owner can add new users.'
    
    if reply:
        update.message.reply_text(reply)

def removeUser(update, context):
    if UService.isTheOwner(update):
        typed_user = update.message.text.replace(
            '/removeuser', '').strip().lower()
        if typed_user != '':
            UService.removeUser(typed_user)
            reply = 'user removed!'
        else:
            reply = 'You need to spcify a telegram name including @.'
    else:
        reply = 'You don\'t have permission. Only the owner can add new users.'

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
        update.message.reply_text(
            f'You don\'t have permission to use this Bot.')
        return

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

if __name__ == '__main__':
    main()
