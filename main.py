
import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        token = os.getenv('telegram_token')
        if token is None:
            logger.error('Set "telegram_token" environment variable.')
            logger.error('export telegram_token=example_token')
            exit(os.EX_CONFIG)
        self.updater = Updater(token, use_context=True)
        self.set_commands_handlers()
    
    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def text_to_channel(self, chat_id, text):
        self.updater.bot.sendMessage(chat_id=chat_id, text=text)
    
    def set_commands_handlers(self):
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler("start", self.on_start))
        dp.add_handler(CommandHandler("help", self.on_help))

        dp.add_handler(MessageHandler(Filters.text, self.on_unknown))
        dp.add_error_handler(self.on_error)
    
    def on_start(self, update, context):
        update.message.reply_text('on /start')

    def on_help(self, update, context):
        update.message.reply_text('on /help')

    def on_unknown(self, update, context):
        update.message.reply_text(f'on unknown command "{update.message.text}"')

    def on_error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    bot = Bot()
    bot.run()