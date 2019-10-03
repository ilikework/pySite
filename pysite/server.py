
#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import tornado.ioloop
import tornado.web
import sqlite3
import os.path
import datetime

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

    def selectNote():
        db = sqlite3.connect('notes.db')
        strsql = "select name,message,chgdate from note"
        cursor = db.execute(strsql)
        db.close()
        return cursor


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

        #self.render("result.html",
        #            len_body = len_body
        #            )

class addNoteHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("add.html")

    def post(self):
        name = self.get_argument('name')
        message = self.get_argument('message')

        db = dbEngine()
        if db.addNote(name,message):
            self.render("add_success.html")

class listNoteHandler(tornado.web.RequestHandler):
    def get(self):
        db = dbEngine()
        notes = db.selectNote()
        self.render("list_note.html",notes=notes)

class testTableHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("raytableSelDemo.html")

application = tornado.web.Application(
    [
    (r"/", MainHandler),
    (r"/add", addNoteHandler),
    (r"/note", listNoteHandler),
    (r"/testTable", testTableHandler)
    ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
)

if __name__ == "__main__":
    application.listen(1888)
    print("Server is up ...")
    tornado.ioloop.IOLoop.instance().start()