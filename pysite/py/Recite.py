#import sys, getopt
#import re
import os
import sqlite3
#import os.path
import datetime

class dbReciteEngine():

    def __init__(self):
        if not os.path.isfile('recite.db'):
            self.__init_db()

    def __get_db(self):
        return sqlite3.connect('recite.db')

    def __get_now_string(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __init_db(self):
        db =self.__get_db()
        c = db.cursor()
        c.execute('create table words (id integer primary key, book_id integer, word text, meaning text, chgdate date)')
        c.execute('create table users (id integer primary key, user text, chgdate date)')
        c.execute('create table books (id integer primary key, book text, chgdate date)')
        c.execute("create table recite_records (word_id integer not null ,user_id integer not null , book_id integer not null , learn_count integer, correct_count integer, chgdate date, " \
                  "primary key(word_id,user_id,book_id) )" )
        db.commit()
        db.close()

    def addUser(self,user):
        user_obj = self.selectUser(user)
        if user_obj != None:
            return user_obj

        db =self.__get_db()
        strsql = "insert into users(user,chgdate)  values('{}','{}')".format(user,self.__get_now_string())
        db.execute(strsql)
        db.commit()
        db.close()
        return self.selectUser(user)

    def isExitUserId(self,id):
        db =self.__get_db()
        strsql = "select count(1) from users where id='{}'".format(id)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def isExitUser(self,user):
        db =self.__get_db()
        strsql = "select count(1) from users where user='{}'".format(user)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def editUser(self,id,user):
        if isExitUser(user):
            return False

        db =self.__get_db()
        strsql = "update users set user = '{}' where id = {}".format(user,id)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def delUser(self,id,bDelRecord):
        # delete recite record which belong to the user.
        if bDelRecord:
             delUserReciteRecords(id)

        # delete user.
        db =self.__get_db()
        strsql = "delete from users where id = {}".format(id)
        db.execute(strsql)

        db.commit()
        db.close()
        return True

    def selectUserById(self,id):
        user_obj = None
        db =self.__get_db()
        strsql = "select id, user,chgdate from users where id={}".format(id)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            user_obj = {"id":row[0],"user":row[1],"chgdate":row[2]}
            break
        db.close()
        return user_obj 


    def selectUser(self,user):
        user_obj = None
        db =self.__get_db()
        strsql = "select id, user,chgdate from users where user = '{}'".format(user)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            user_obj = {"id":row[0],"user":row[1],"chgdate":row[2]}
            break
        db.close()
        return user_obj 

    def selectUsers(self):
        db =self.__get_db()
        strsql = "select id, user,chgdate from users order by chgdate"
        cursor = db.execute(strsql)
        users = []
        i = 0
        for row in cursor.fetchall():
            i +=1
            user = {"id":row[0],"no":str(i),"code":row[1],"chgdate":row[2]}
            users.append(user)
        db.close()
        return users 

    def addBook(self,book):
        db =self.__get_db()
        if self.isExitBook(book):
            return False
        strsql = "insert into books(book,chgdate)  values('{}','{}')".format(book,self.__get_now_string())
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def isExitBookID(self,bookId):
        db =self.__get_db()
        strsql = "select count(1) from books where id={}".format(bookId)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def isExitBook(self,book):
        db =self.__get_db()
        strsql = "select count(1) from books where book='{}'".format(book)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def editBook(self,id,book):
        if isExitBook(book):
            return False
        db =self.__get_db()
        strsql = "update books set book = '{}' where id={}".format(id,book)
        db.execute(strsql)
        db.commit()
        return True

    def delBook(self,id,bDelWords):
        # 1. delete words which belong to the user.
        if bDelWords:
            delBookWords(id)
            delBookReciteRecords(id)
        
        # 2. delete book.
        db =self.__get_db()
        strsql = "delete from books where id = {}".format(id)
        db.execute(strsql)

        db.commit()
        db.close()
        return True

    def selectBook(self,id):
        book = {}
        db =self.__get_db()
        strsql = "select id, book,chgdate from books where id = {}".format(id)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            book = {"id":row[0],"book":row[1],"chgdate":row[2]}
            break
        db.close()
        return book

    def selectBooks(self):
        db =self.__get_db()
        strsql = "select id, book,chgdate from books order by chgdate"
        cursor = db.execute(strsql)
        books = []
        i = 0
        for row in cursor.fetchall():
            i +=1
            book = {"id":row[0],"no":str(i),"book":row[1],"chgdate":row[2]}
            books.append(book)
        db.close()
        return books

    def delUserReciteRecords(self,userId):
        db =self.__get_db()
        strsql = "delete from recite_records where user_id = {}".format(userId)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def delBookReciteRecords(self,bookId):
        db =self.__get_db()
        strsql = "delete from recite_records where book_id = {}".format(bookId)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def delBookWords(self,bookId):
        db =self.__get_db()
        strsql = "delete from words where book_id = {}".format(bookId)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def addWord(self,bookId,word, meaning):
        db =self.__get_db()
        if self.isExitWord(bookId,word):
            return False
        strsql = "insert into words(book_id, word,meaning,chgdate)  values('{}','{}','{}','{}')".format(bookId,word,meaning,self.__get_now_string())
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def editWord(self,bookId,wordId,word,meaning):
        if self.isExitWordExpectMe(bookId,wordId,word):
            return False
        db =self.__get_db()
        strsql = "update words set word = '{}' , meaning = '{}',chgdate = '{}' where id={}".format(word,meaning,self.__get_now_string(),wordId)
        db.execute(strsql)
        db.commit()
        db.close()
        return True

    def isExitWordId(self,id):
        db =self.__get_db()
        strsql = "select count(1) from words where id = {} ".format(id)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def isExitWord(self,bookId,word):
        if not self.isExitBookID(bookId):
            return False
        db =self.__get_db()
        strsql = "select count(1) from words where book_id = {} and word='{}'".format(bookId,word)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def isExitWordExpectMe(self,bookId,wordId,word):
        if not self.isExitBookID(bookId):
            return False
        db =self.__get_db()
        strsql = "select count(1) from words where book_id = {} and word='{}' and id <>{} ".format(bookId,word,wordId)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                return True
        return False

    def delWord(self,id):
        db =self.__get_db()
        # delete from recite_records 
        strsql = "delete from recite_records where word_id = {}".format(id)
        db.execute(strsql)

        # delete from words
        strsql = "delete from words where id = {}".format(id)
        db.execute(strsql)

        db.commit()
        db.close()
        return True

    def selectWords(self,bookId):
        db =self.__get_db()
        strsql = "select id, word,meaning,chgdate from words where book_id = '{}' order by id".format(bookId)
        cursor = db.execute(strsql)
        words = []
        i = 0
        for row in cursor.fetchall():
            i +=1
            word = {"id":row[0],"no":str(i),"word":row[1],"meaning":row[2],"chgdate":row[3] }
            words.append(word)
        db.close()
        return words

    def selectWords(self,bookId,userId):
        db =self.__get_db()
        strsql = "select a.id, a.word,a.meaning,ifnull(b.learn_count,0),ifnull(b.correct_count,0),a.chgdate " \
                " from words a left outer join recite_records b ON  a.id=b.word_id and b.user_id = '{}' and a.book_id = b.book_id " \
                " where a.book_id = '{}' order by a.id".format(userId,bookId)
        cursor = db.execute(strsql)
        words = []
        i = 0
        for row in cursor.fetchall():
            i +=1
            word = {"id":row[0],"no":str(i),"word":row[1],"meaning":row[2], "learn_count":row[3], "correct_count":row[4],"chgdate":row[5]}
            words.append(word)
        db.close()
        return words

    def selectWord(self,wordId):
        db =self.__get_db()
        strsql = "select id, word,meaning from words where id = {}".format(wordId)  
        cursor = db.execute(strsql)
        word = {}
        for row in cursor.fetchall():
            word = {"id":row[0],"word":row[1],"meaning":row[2]}
            break;
        db.close()
        return word

    def addReciteRecord(self,wordId,userId,bookId,bCorrect):
        if not self.isExitUserId(userId):
            return False
        if not self.isExitBookID(bookId):
            return False
        if not self.isExitWordId(wordId):
            return False
        db =self.__get_db()
        bExist = False
        strsql = "select count(1) from recite_records where word_id = {} and user_id = {} and book_id = {} ".format(wordId,userId,bookId)
        cursor = db.execute(strsql)
        for row in cursor.fetchall():
            if int(row[0])>0:
                bExist = True
                break

        if bExist:
            str = "learn_count = learn_count +1"
            if bCorrect:
                str = str + ", correct_count = correct_count + 1"

            strsql = "update recite_records set {} where word_id = {} and user_id = {} and book_id = {} ".format(str,wordId,userId,bookId)
        else:
            learn_count = 1
            correct_count = 0
            if bCorrect:
                correct_count = 1
            strsql = " insert into recite_records(word_id,user_id,book_id,learn_count,correct_count,chgdate) " \
                     " values('{}','{}','{}','{}','{}','{}')".format(wordId,userId,bookId,learn_count,correct_count,self.__get_now_string())
        db.execute(strsql)
        db.commit()
        db.close()
        return True


class Recite(object):
    """description of class"""
    def createQuestions(self,bookId,userId,wordId):
        db =dbReciteEngine()
        word = selectWord(wordId)
        words = db.selectWords(bookId,userId)
        answer = -1
        opts = []
        if len(words)>=4:
            while(True):
                opt = random.randint(0,len(words)-1)
                if opt in opts:
                    continue
                else:
                    opts.append(opt)
                if len(opts)==3:
                    break

        meanings = []
        for opt in opts:
            n = random.randint(1,len(opts))
            while(1):
                if meanings[n]==None:
                    meanings[n] = words[opt]["meaning"]
                    break
        for i in range(0,3):
            if meanings[i]==None:
                meaning[i] = word["meaning"]
                answer = i
        question = {"question":word[word],"meanings":meanings,"answer":answer}
        return question

    def createBook(self,book):
        db =dbReciteEngine()
        return db.addBook(book)

    def delBook(self,bookId,bDelWords):
        db =dbReciteEngine()
        return db.delBook(bbookId,bDelWords)
    
    def editBook(self,bookId,book):
        db =dbReciteEngine()
        return db.editBook(bbookId,book)

    def selectBook(self,bookId):
        db =dbReciteEngine()
        return db.selectBook(bookId)

    def selectBooks(self):
        db =dbReciteEngine()
        return db.selectBooks()

    def createUser(self,user):
        db =dbReciteEngine()
        return db.addUser(user)

    def isExitUser(self,user):
        db =dbReciteEngine()
        return db.isExitUser(user)

    def selectUser(self,userId):
        db =dbReciteEngine()
        return db.selectUserById(userId)

    def delUser(self,userId,bDelRecord):
        db =dbReciteEngine()
        return db.delUser(userId,bDelRecord)

    def editUser(self,userId,user):
        db =dbReciteEngine()
        return db.editUser(userId,user)

    def createWord(self,bookId,word,meaning):
        db =dbReciteEngine()
        return db.addWord(bookId,word,meaning)

    def selectWord(self,wordId):
        db = dbReciteEngine()
        return db.selectWord(wordId)

    def editWord(self,bookId,wordId,word,meaning):
        db =dbReciteEngine()
        return db.editWord(bookId,wordId,word,meaning)

    def selectWords(self,bookId,userId):
        db = dbReciteEngine()
        return db.selectWords(bookId,userId)

    def delWord(self,wordId):
        db =dbReciteEngine()
        return db.delWord(wordId)

    def createReciteRecord(self,wordId,userId,bookId,bCorrect):
        db =dbReciteEngine()
        return db.addReciteRecord(wordId,userId,bookId,bCorrect)
