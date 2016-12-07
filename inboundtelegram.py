from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import gearman
import json
AUTH_TOKEN = "285351123:AAFevc78WhbcwguBbOZY8MY09jS5l-NVb9E"
# bot.sendPhoto(chat_id=chat_id,photo = open('img.png','rb'))
class first_bot:
    def __init__(self):
        self.updater = Updater(token = AUTH_TOKEN )
        self.dispatcher = self.updater.dispatcher
        self.gm_client = gearman.GearmanClient(['localhost:4730'] )
        logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level = logging.INFO )

    def run(self, bot_value, update_value):
        global bot
        global update
        bot = bot_value
        update = update_value
        ChatMsg = update.message.text
        completed_task = self.gm_client.submit_job('Gator',str(ChatMsg))
        result = json.loads(completed_task.result)
        if completed_task.state == 'COMPLETE':
            bot_value.sendPhoto(chat_id=update.message.chat_id,photo = open('img.png','rb'))        

if __name__ == '__main__':
        telebot = first_bot()
        echo_handler = MessageHandler([Filters.text],telebot.run)
        telebot.dispatcher.add_handler(echo_handler)
        telebot.updater.start_polling(poll_interval = 1.0)
        telebot.updater.idle()
