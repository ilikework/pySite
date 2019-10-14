import requests
#import sys, getopt
#import re
import os
import sqlite3
#import os.path
import datetime

pattern = '.*="(.*?)".*'
url = 'http://hq.sinajs.cn/list='
FORMAT_GREEN = "<font color=\"green\">{}</font>"
FORMAT_RED = "<font color=\"red\">{}</font>"

class dbStockEngine():

    def __init__(self):
        if not os.path.isfile('stock.db'):
            self.__init_db()

    def __get_db(self):
        return sqlite3.connect('stock.db')

    def __init_db(self):
        db =self.__get_db()
        c = db.cursor()
        c.execute('create table stock (id integer primary key, code text, message text, chgdate date)')
        db.commit()
        db.close()

    def addStock(self,code,message):
        db =self.__get_db()
        if self.isExitStock(code):
            return False
        strsql = "insert into stock(code,message,chgdate)  values('{}','{}','{}')".format(code,message,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def isExitStock(self,code):
        db =self.__get_db()
        strsql = "select count(1) from stock where code='{}'".format(code)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def delStock(self,id):
        db =self.__get_db()
        strsql = "delete from stock where id = {}".format(id)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def selectStocks(self):
        db =self.__get_db()
        strsql = "select id, code,message,chgdate from stock order by chgdate"
        cursor = db.execute(strsql)
        stocks = []
        i = 0
        for row in cursor.fetchall():
            i +=1
            stock = {"id":row[0],"no":str(i),"code":row[1],"message":row[2],"chgdate":row[3]}
            stocks.append(stock)
        db.close()
        return stocks 

class Stock(object):

    def __get_stocks(self):
        stocks = []
        db = dbStockEngine()
        stocks = db.selectStocks()

        return stocks

    def __change_stock_code(self,code):
        if len(code)==6:
            if code[0]=='6':
                return "s_sh" + code
            return "s_sz" + code
        return code

    def get_stock_info(self):
        stock_info = []
        stocks = self.__get_stocks()
        i = 0
        for stock in stocks:
            response = requests.get(url+self.__change_stock_code(stock["code"]))
            if response.status_code==200:
                match_result = re.match(pattern, response.text)
                info = match_result.group(1).split(',')
                i +=1
                if float(info[2])>0:
                    stock_info.append({    'id' :stock["id"] 
                                        , 'no':FORMAT_RED.format(str(i))
                                        ,'name':FORMAT_RED.format(info[0])
                                        ,'price':FORMAT_RED.format(info[1])
                                        ,'rise':FORMAT_RED.format(info[2])
                                        ,'rise_persent':FORMAT_RED.format(info[3])
                                        ,'amount':FORMAT_RED.format(info[4])
                                        ,'sum':FORMAT_RED.format(info[5])})
                elif float(info[2])<0:
                    stock_info.append({   'id' :stock["id"] 
                                        , 'no':FORMAT_GREEN.format(str(i))
                                        ,'name':FORMAT_GREEN.format(info[0])
                                        ,'price':FORMAT_GREEN.format(info[1])
                                        ,'rise':FORMAT_GREEN.format(info[2])
                                        ,'rise_persent':FORMAT_GREEN.format(info[3])
                                        ,'amount':FORMAT_GREEN.format(info[4])
                                        ,'sum':FORMAT_GREEN.format(info[5])})
                else:
                    stock_info.append({  'id' :stock["id"] 
                                        , 'no':str(i)
                                        ,'name':info[0]
                                        ,'price':info[1]
                                        ,'rise':info[2]
                                        ,'rise_persent':info[3]
                                        ,'amount':info[4]
                                        ,'sum':info[5]})

        return stock_info;

    def add_stock(self,code,message):
        db = dbStockEngine()
        stocks = db.addStock(code,message)
        return True

    def delete_stock(self,id):
        db = dbStockEngine()
        stocks = db.delStock(id)
        return True
#print(type(response)) # <class 'requests.models.Response'>
#print(response.status_code) # 200
#print(type(response.text)) # <class 'str'>
#print(response.text)
#print(response.cookies) # <RequestsCookieJar[<Cookie BDORZ=27315 for >]>

