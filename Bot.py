import config

import datetime

import DB

import telebot

import cherrypy

daysOfWeek={'понедельник':1, 'вторник':2, 'среда':3, 'четверг':4, 'пятница':5, 'суббота':6, 'воскресенье':0}

queriesOfPara={'пара':1,'какая сейчас пара':2,'какая у нас пара':3,'что за пара':4,'шо по паре':5,'у нас есть пара':6 }

time1 ={'сколько время':1,'который час':2,'время':3,'time':4}
bot = telebot.TeleBot(config.token)


WEBHOOK_HOST = '109.86.1.91'
WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '109.86.1.91'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './SSL.cer' # Путь к сертификату
WEBHOOK_SSL_PRIV = './Keys_Pr.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})




# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
        
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
        
#Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

"""if __name__ == '__main__':
    bot.polling(none_stop=True)"""
