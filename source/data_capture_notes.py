import os
import sqlite3
import sys
from tkinter import messagebox
db=""
def get_Lessons():
    print (db)
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_ID, Lesson_Title from Magic_Science_Lessons"
    cur.execute(sql)
    rows = cur.fetchall()
    list_lessons = []
    for element in rows:
        list_lessons.append(element)
    connection.commit()
    connection.close()
    return list_lessons

def get_Lesson_Dictionary(file_root,lesson_id):
        connection = sqlite3.connect(file_root+os.path.sep+"MagicRoom.db")
        cur = connection.cursor()
        sql = "select * from Magic_Science_Lessons where Lesson_ID =?"
        cur.execute(sql,(lesson_id,))
        p = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        r = p[0]
        print (r)
        cur.connection.close()
        return r


