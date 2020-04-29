import json
import unittest,source.snapshot_controller
import sqlite3, configparser

class TestSnapshotMethods(unittest.TestCase):
    json_str = ""

    def setUp(self) -> None:

        config = configparser.RawConfigParser()
        config.read("../../magic.cfg")
        self.data_root = config.get("section1","dataroot")
        json_lesson = self.create_json()
    def test_title_conversion(self):

        pdf_gen = source.snapshot_controller.MagicSnapshotController(json_str).getSnapshotView()
        pdf_gen.create_title_notes()
        pdf_gen.create_factual_notes()
        pdf_gen.create_application_notes()
        pdf_gen.create_assessment_notes()
    def test_text_conversion(self):
        pass
    def test_file_creation(self):
        pass

    def create_json(self):
        global json_str
        connection = sqlite3.connect(self.data_root)
        cur = connection.cursor()
        sql = "select * from Magic_Science_Lessons where Lesson_ID =20"
        cur.execute(sql)
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        json_str = json.dumps(r)







