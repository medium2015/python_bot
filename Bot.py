import config

import datetime

import DB

import telebot

daysOfWeek={'понедельник':1, 'вторник':2, 'среда':3, 'четверг':4, 'пятница':5, 'суббота':6, 'воскресенье':0}

queriesOfPara={'пара':1,'какая сейчас пара':2,'какая у нас пара':3,'что за пара':4,'шо по паре':5,'у нас есть пара':6 }

time1 ={'сколько время':1,'который час':2,'время':3,'time':4}
bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    print ("User: %s says: %s" % (message.chat.id, message.text)) 
    if (str(message.text).lower() in daysOfWeek):
        result = DB.SQLighter("D:\DB Browser for SQLite\Raspisanie.db").select_all(daysOfWeek[str(message.text).lower()])
        if len(result):
            for i in range(len(result)):
                bot.send_message(message.chat.id, "{4} {2}-{3} ауд. {5}".format(*result[i]))
        else:
            bot.send_message(message.chat.id, "Сегодня занятий нет")
    elif (str(message.text).lower() in queriesOfPara):     
        para=DB.SQLighter("D:\DB Browser for SQLite\Raspisanie.db").select_para()
        if len(para):
            bot.send_message(message.chat.id, "{4} {2}-{3} ауд. {5}".format(*para[0]))
        else:
            bot.send_message(message.chat.id, "Сейчас пар нет")
    elif (str(message.text).lower() in time1): 
        bot.send_message(message.chat.id, datetime.datetime.strftime(datetime.datetime.now(),"%H:%M"))
    elif (message.text=='/start'):
        bot.send_message(message.chat.id, 'Привет, я чат-бот, который показывает расписание группы КН-21. Мои команды:'+'\n'+'/help')
    elif (message.text=='/help'):
        bot.send_message(message.chat.id, 'Для того, чтобы узнать расписание на какой-либо день, отправь мне сообщение с днём недели. Чтобы узнать, какая у тебя сейчас пара, так меня и спроси.')
    else:
        bot.send_message(message.chat.id, message.text) 
        
if __name__ == '__main__':
    bot.polling(none_stop=True)
