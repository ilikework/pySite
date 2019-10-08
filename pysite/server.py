
#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, getopt
import os
import tornado.ioloop
import tornado.web
import sqlite3
import os.path
import datetime
import json
from py.Stock import Stock

class dbEngine():

    def __init__(self):
        if not os.path.isfile('notes.db'):
            self.__init_db()

    def __init_db(self):
        db = sqlite3.connect('notes.db')
        c = db.cursor()
        c.execute('create table note (id integer primary key, name text, message text, chgdate date)')
        db.commit()
        db.close()

    def addNote(self,name,message):
        db = sqlite3.connect('notes.db')
        strsql = "insert into note(name,message,chgdate)  values('{}','{}','{}')".format(name,message,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def updateNote(self,id,name,message):
        db = sqlite3.connect('notes.db')
        strsql = "update note set name='{}', message='{}', chgdate = '{}' where id = {}".format(name,message,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),id)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def delNote(self,id):
        db = sqlite3.connect('notes.db')
        strsql = "delete from note where id = {}".format(id)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def selectNote(self):
        db = sqlite3.connect('notes.db')
        strsql = "select id, name,message,chgdate from note order by chgdate"
        cursor = db.execute(strsql)
        notes = []
        i = 0
        for row in cursor.fetchall():
            i +=1
            note = {"id":row[0],"no":str(i),"name":row[1],"message":row[2],"chgdate":row[3]}
            notes.append(note)
        db.close()
        return notes 

    def selectOneNote(self,id):
        db = sqlite3.connect('notes.db')
        strsql = "select name,message from note where id = {} ".format(id)
        cursor = db.execute(strsql)
        name =''
        message =''
        for row in cursor.fetchall():
            name = row[0]
            message = row[1]
        db.close()
        return name,message 

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        db = dbEngine()
        notes = db.selectNote()
        self.render("list_note.html",notes=notes)

        #self.render("result.html",
        #            len_body = len_body
        #            )

class addNoteHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("add_note.html")

    def post(self):
        name = self.get_argument('name')
        message = self.get_argument('message')

        db = dbEngine()
        if db.addNote(name,message):
            self.render("add_success.html")

class editNoteHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id')
        db = dbEngine()
        name,message = db.selectOneNote(id)
        self.render("edit_note.html",id=id,name=name,message=message)

    def post(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        message = self.get_argument('message')
        db =dbEngine()
        if db.updateNote(id,name,message):
            notes = db.selectNote()
            self.render("list_note.html",notes=notes)

class delNoteHandler(tornado.web.RequestHandler):

    def post(self):
        id = self.get_argument('id')

        db = dbEngine()
        if db.delNote(id):
            self.write("0")

class listNoteHandler(tornado.web.RequestHandler):
    def get(self):
        db = dbEngine()
        notes = db.selectNote()
        self.render("list_note.html",notes=notes)

class testTableHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("raytableSelDemo.html")

class testTTSHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test_tts.html")

class stockHandler(tornado.web.RequestHandler):
    def get(self):
        stock_api = Stock()
        stocks = stock_api.get_stock_info()
        print(stocks)
        self.render("stock.html",stocks=stocks)

application = tornado.web.Application(
    [
    (r"/", listNoteHandler),
    (r"/note", listNoteHandler),
    (r"/add_note", addNoteHandler),
    (r"/edit_note", editNoteHandler),
    (r"/delete_note", delNoteHandler),
    (r"/testTable", testTableHandler),
    (r"/testTTS", testTTSHandler),
    (r"/stock", stockHandler)
    ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
)

def main(argv):
    port = 1888;
    try:
      opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
      print("server.py -p <port>")
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print("server.py -p <port>")
         sys.exit()
      elif opt in ("-p", "--port"):
         port = arg

    application.listen(port)
    print("Server is up on port {}...".format(port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main(sys.argv[1:])

