from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import ephem
import datetime

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def planet_place(bot, update):
    user_text = update.message.text.split()
    try:
        user_planet = user_text[1]
        d = datetime.datetime.now()
        if hasattr(ephem, user_planet):
            const = getattr(ephem, user_planet)(d)
            result = ephem.constellation(const)
            update.message.reply_text(result)
            logging.info(result)
        else:
            reply_to_user = "Эта планета или спутник находится вне солнечной системы"
            update.message.reply_text(reply_to_user)
    except IndexError:
        update.message.reply_text('Вы не ввели название планеты')


def greet_user(bot, update):
    text = 'Вызван /start'
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = "Привет, {}! Ты написал : {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s Chat id $s Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info("Бот запускается")

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", planet_place))

    mybot.start_polling()
    mybot.idle()


main()
