import logging
import tkinter as tk
import traceback
from tkinter import filedialog
from textwrap import wrap
import os

from PIL import Image
from reportlab.pdfgen import canvas

import data_capture_notes

logger = logging.getLogger("MagicLogger")
file_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
db = file_root + os.path.sep + "MagicRoom.db"

class PDFUtils():
    def __init__(self, lesson_id,filename,*args, **kwargs):
        self.lesson_id = lesson_id
        self.file_root = file_root
        self.lesson_text_full =""
        data_capture_notes.db = db
        self.lesson_data_dictionary = data_capture_notes.get_Lesson_Dictionary(file_root, lesson_id)
        self.lesson_root = self.file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
            self.lesson_data_dictionary.get("Lesson_ID"))
        self.notes_file = canvas.Canvas(filename)
        self.notes_file.setTitle("Learning Room Lesson Notes " + str(self.lesson_data_dictionary.get("Lesson_ID")))
        self.create_title_notes()
        self.create_factual_notes()
        self.create_application_notes()
        self.create_assessment_notes()
        self.create_canvas_image()

    def add_file(self,fileroot,window):
        filename_img_title_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Image',parent=window)
        filename_img_title = os.path.basename(filename_img_title_full)
        print(filename_img_title)
        return filename_img_title_full, filename_img_title

    def create_title_notes(self):
        
              self.Title_Font = self.notes_file.setFont("Helvetica", 16)
              self.notes_file.drawCentredString(300, 820, self.lesson_data_dictionary.get("Lesson_Title"))
              self.notes_file.setFont("Helvetica", 8)
              self.notes_file.setFillColorRGB(0,0,1) 
              self.notes_file.drawCentredString(300,810,"http://www.wondersky.in")
              self.notes_file.setFillColorRGB(0,0,0) 
              link_width = self.notes_file.stringWidth("http://www.wondersky.in")
              link_rect = (220,810,290,795)
              self.notes_file.linkURL("http://www.wondersky.in", link_rect)
              self.Text_Font = self.notes_file.setFont("Helvetica", 12)
              self.title_text_object = self.notes_file.beginText()
              self.title_text_object.setTextOrigin(50,800)
              self.title_text_object.setHorizScale(90)
              title_Text = self.lesson_data_dictionary.get("Title_Running_Notes")
              self.lesson_text_full += "Introduction.\n"+title_Text+".\n"
              wraped_Text = " ".join(wrap(title_Text, 60, replace_whitespace=False))
              self.title_text_object.textLines(wraped_Text)
              self.notes_file.drawText(self.title_text_object)
              try:
                 self.notes_file.drawImage(self.lesson_root+os.path.sep+"images"+os.path.sep+self.lesson_data_dictionary.get("Title_Image"),width=300,height=300,x=150,y = self.title_text_object.getY()-300)

              except:
                 logger.exception("Image Most likely empty or invalid - Title")
              self.notes_file.drawCentredString(300, 800-300-self.title_text_object.getX()-50-150-50,"Video File Used : "+
                                                self.lesson_data_dictionary.get("Title_Video"))

              self.notes_file.showPage()
       



    def create_factual_notes(self):
      self.notes_file.setFont("Helvetica", 16)
      self.notes_file.drawCentredString(300, 820, "Terms and Definitions")
      i = 0
      self.lesson_text_full += "Definitions."
      while i < 3:
        factual_text_object = self.notes_file.beginText()
        factual_text_object.setTextOrigin(150,(700-i*210))
        factual_text_object.setHorizScale(60)
        factual_text_object.setFont("Helvetica", 16)
        factual_text_object.textLine(self.lesson_data_dictionary.get("Factual_Term"+str(i+1)))
        term_text = self.lesson_data_dictionary.get("Factual_Term" + str(i + 1))
        factual_text_object.setFont("Helvetica", 12)
        factual_text = self.lesson_data_dictionary.get("Factual_Term"+str(i+1)+"_Description")
        self.lesson_text_full += term_text+"."+factual_text+"."
        wraped_text = "\n".join(wrap(factual_text, 30, replace_whitespace=False))
        factual_text_object.textLines(wraped_text)
        self.notes_file.drawText(factual_text_object)
        try:
            self.notes_file.drawImage(self.lesson_root+os.path.sep+"images"+os.path.sep + self.lesson_data_dictionary.get("Factual_Image"+str(i+1)),
                                  width=200, height=200,
                                  x=factual_text_object.getX()+150, y=factual_text_object.getY()-100)
        except:
             logger.exception("Image Most likely empty or invalid - Factual")
        i +=1

      self.notes_file.showPage()



    def create_application_notes(self):
      self.notes_file.setFont("Helvetica", 16)
      self.notes_file.drawCentredString(300, 820, "Skill Building")
      number_of_steps = int(self.lesson_data_dictionary.get("Application_Steps_Number"))
      i=0
      self.lesson_text_full += "Skill Building Steps."
      while i < number_of_steps:
        application_text_object = self.notes_file.beginText()
        application_text_object.setTextOrigin(100, (750 - i * 90))
        application_text_object.setHorizScale(70)
        application_text_object.setFont("Helvetica-Bold", 12)
        step_text = str(i+1)+". "+self.lesson_data_dictionary.get("Application_Step_Description_" + str(i + 1))
        self.lesson_text_full += step_text + "."
        wraped_text = "\n".join(wrap(step_text, 50, replace_whitespace=False))
        application_text_object.textLines(wraped_text)
        self.notes_file.drawText(application_text_object)
        image_name = self.lesson_data_dictionary.get("Application_Steps_Widget_" + str(i + 1))
        if ( image_name is not None and image_name.strip() != ""):
               try:
                     self.notes_file.drawImage(self.lesson_root+os.path.sep+"images"+os.path.sep+ self.lesson_data_dictionary.get("Application_Steps_Widget_" + str(i + 1)),
                                  width=50, height=50,
                                  x=application_text_object.getX() + 50, y=application_text_object.getY() -40)
               except:
                   logger.exception("Application Image Empty")

        i += 1
      link_text_object = self.notes_file.beginText()
      link_text_object.setTextOrigin(100,100)
      link_text_object.setHorizScale(70)
      link_text_object.setFont("Helvetica-Bold", 12)
      link_text_object.textLine(self.lesson_data_dictionary.get("Apply_External_Link"))
      print(self.lesson_data_dictionary.get("Apply_External_Link"))
      self.notes_file.drawText(link_text_object)
      self.notes_file.showPage()

    def create_assessment_notes(self):
        self.notes_file.setFont("Helvetica", 16)
       
        self.notes_file.drawCentredString(300, 820, "Assessment")
        assessment_text = self.lesson_data_dictionary.get("IP_Questions")
        assessment_text_object = self.notes_file.beginText()
        assessment_text_object.setTextOrigin(50, 750)
        assessment_text_object.setHorizScale(75)
        assessment_text_object.setFont("Helvetica", 12)
        wraped_text = " ".join(wrap(assessment_text, 80,replace_whitespace=False))
        assessment_text_object.textLines(wraped_text)
        self.notes_file.drawText(assessment_text_object)
        self.notes_file.showPage()


    def create_canvas_image(self):
        self.notes_file.setFont("Helvetica", 16)
        self.notes_file.drawCentredString(300, 820, "Skill Board")
        list_files = os.listdir(self.lesson_root+os.path.sep+"saved_boards")
        file_index = 1
        for file in list_files:
            imageobject =Image.open( self.lesson_root+os.path.sep+"saved_boards"+os.path.sep+file)
            imageobject.resize((500,500),Image.ANTIALIAS)
            imageobject.save(self.lesson_root+os.path.sep+"saved_boards"+os.path.sep+file)
            try:
                self.notes_file.drawImage(
                self.lesson_root+os.path.sep+"saved_boards"+os.path.sep+file,
                width=500, height=500,
                x=50,y =150)
            except:
                logger.exception("Invalid Board Image")
            file_index += 1
            self.notes_file.showPage()
        self.notes_file.save()
