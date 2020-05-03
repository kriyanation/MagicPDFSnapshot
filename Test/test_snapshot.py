import json
import os
import unittest
import sqlite3, configparser,snapshot_view

class TestSnapshotMethods(unittest.TestCase):


    def setUp(self) -> None:

        config = configparser.RawConfigParser()
        config.read("../../magic.cfg")
        self.file_root = config.get("section1","file_root")
        self.r ={ }
        self.create_json()

    def test_title_conversion(self):

        pdf_gen = snapshot_view.SnapshotView(self.r,self.file_root)
        pdf_gen.create_title_notes()
        pdf_gen.create_factual_notes()
        pdf_gen.create_application_notes()
        pdf_gen.create_assessment_notes()
        pdf_gen.create_canvas_image()
    def test_text_conversion(self):
        pass
    def test_file_creation(self):
        pass

    def create_json(self):

        connection = sqlite3.connect(self.file_root+os.path.sep+"MagicRoom.db")
        cur = connection.cursor()
        sql = "select * from Magic_Science_Lessons where Lesson_ID =24"
        cur.execute(sql)
        p = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        self.r = p[0]
        print (self.r)
        cur.connection.close()








