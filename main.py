
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('on /start')


def help(update, context):
    update.message.reply_text('on /help')


def echo(update, context):
    update.message.reply_text(f'on unknown command {update.message.text}')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def text_to_channel(updater, text, chat_id='@colykxer'):
    updater.bot.sendMessage(chat_id=chat_id, text='Some content')


def main():
    updater = Updater("", use_context=True)
    text_to_channel(updater, 'text')

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

class Bot:
    def __init__(self):
        pass

        

if __name__ == '__main__':
    main()