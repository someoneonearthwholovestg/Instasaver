import telebot
import config
import datetime

bot = telebot.TeleBot(config.token_telegram)

def logger(msg):
    if (type(msg) is telebot.types.Message):
        logData = datetime.datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
        log = config.logForm.format(logData, msg.chat.first_name, msg.chat.last_name, msg.chat.username,msg.text)
    else:
        log = msg

    try:
        print(log)
        config.logFile(log)
    except Exception as ex:
        config.logFile(msg=ex)



@bot.message_handler(commands=["start"])
def greeting(message):
    logger(msg=message)
    bot.send_message(message.chat.id, text="Hello, {}!".format(message.chat.first_name))




if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as ex:
        config.logFile(msg=ex)