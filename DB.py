import sqlite3
class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor() 
    def select_all(self,inputDay):
        """ Получаем все пары """
        with self.connection:
            self.cursor.execute('SELECT * FROM timeTable where weekDay='+str(inputDay))
            return self.cursor.fetchall()

    def select_para(self):
        """ Получаем пару """
        with self.connection:
            self.cursor.execute("select * from timeTable Where strftime('%H:%M','now') - strftime('%H:%M',startTime)+2>=0 AND strftime('%H:%M',endTime) - strftime('%H:%M','now')-2>=0 and strftime('%w','now')=weekDay")
            return self.cursor.fetchall()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
        
obj = SQLighter
