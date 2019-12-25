import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from news_feed_parser import parse_habr
import telegram

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.token = os.getenv("telegram_token")
        if self.token is None:
            logger.error('Set "telegram_token" environment variable.')
            logger.error("export telegram_token=example_token")
            exit(os.EX_CONFIG)

        self.updater = Updater(self.token, use_context=True)
        self.set_commands_handlers()

        self.news_format = (
            "<b>{title}</b>\n{description}\n\n{link}"
        )

    def local_run(self):
        self.updater.start_polling()
        self.updater.idle()

    def web_run(self):
        port = int(os.environ.get("PORT", 5000))
        self.updater.start_webhook(
            listen="0.0.0.0", port=port, url_path=self.token,
        )
        self.updater.bot.setWebhook(
            "https://colykxer-bot.herokuapp.com/{}".format(self.token)
        )
        self.updater.idle()

    def text_to_channel(self, chat_id, text):
        self.updater.bot.sendMessage(chat_id=chat_id, text=text)

    def set_commands_handlers(self):
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler("start", self.on_start))
        dp.add_handler(CommandHandler("help", self.on_help))
        dp.add_handler(CommandHandler("habr", self.on_habr))

        dp.add_handler(MessageHandler(Filters.text, self.on_unknown))
        dp.add_error_handler(self.on_error)

    def on_start(self, update, context):
        update.message.reply_text("on /start")

    def on_habr(self, update, context):
        news = parse_habr()[0]
        response = self.news_format.format(**news)
        categories = ('<i>#{}</i> ' * len(news['category'])).format(*news['category'])
        categories = '\n\n' + categories
        response += categories
        update.message.reply_text(text=response, parse_mode=telegram.ParseMode.HTML)

    def on_help(self, update, context):
        update.message.reply_text("on /help")

    def on_unknown(self, update, context):
        update.message.reply_text(f'on unknown command "{update.message.text}"')

    def on_error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    bot = Bot()
    bot.local_run()
