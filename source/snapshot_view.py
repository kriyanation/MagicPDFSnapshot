
import os,lesson_list_PDF_notes
import subprocess
import sys
import tkinter as tk
import traceback
from tkinter import messagebox
from reportlab.pdfgen import canvas
from PIL import Image

import data_capture_notes

file_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
db = file_root + os.path.sep + "MagicRoom.db"

class SnapshotView(tk.Toplevel):
    def __init__(self,parent,lesson_id="",filename="",*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.configure(background="gray16")
        self.file_root = file_root
        data_capture_notes.db=db
        self.lesson_id = lesson_id
        self.view_flag = 0
        if lesson_id =="" or lesson_id is None:
            app = lesson_list_PDF_notes.MagicLessonList(bg='beige', fg='firebrick', buttonbg='firebrick', selectmode=tk.SINGLE,
                                         buttonfg='beige', parent=self)

            self.wait_window(app)
            print(self.selected_lessons)
            self.lesson_id = int(self.selected_lessons[0:self.selected_lessons.index(':') - 1].strip())
            self.view_flag=1

            filename = self.file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(self.lesson_id)+os.path.sep+"notes_"+str(self.lesson_id)+".pdf"
        self.lesson_data_dictionary = data_capture_notes.get_Lesson_Dictionary(file_root, self.lesson_id)
        self.lesson_root =  self.file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
            self.lesson_data_dictionary.get("Lesson_ID"))
        self.notes_file = canvas.Canvas(filename)
        self.notes_file.setTitle("Learning Room Lesson Notes "+str(self.lesson_data_dictionary.get("Lesson_ID")))
        self.create_title_notes()
        self.create_factual_notes()
        self.create_application_notes()
        self.create_assessment_notes()
        self.create_canvas_image()
        if self.view_flag == 1:
            try:
                if sys.platform == "win32":
                    os.startfile(filename)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, filename])
            except:
                messagebox.showerror("File open Error",
                                     "File could not be opened. Check if you have Adobe Reader Installed or if the folder has full permissions")

    def create_title_notes(self):
      self.Title_Font = self.notes_file.setFont("Helvetica", 16)
      self.notes_file.drawCentredString(300, 820, self.lesson_data_dictionary.get("Lesson_Title"))
      self.Text_Font = self.notes_file.setFont("Helvetica", 12)
      self.title_text_object = self.notes_file.beginText()
      self.title_text_object.setTextOrigin(50,800)
      self.title_text_object.setHorizScale(90)
      self.title_text_object.textLines(self.lesson_data_dictionary.get("Title_Running_Notes"))
      self.notes_file.drawText(self.title_text_object)
      self.notes_file.drawImage(self.lesson_root+os.path.sep+"images"+os.path.sep+self.lesson_data_dictionary.get("Title_Image"),width=300,height=300,x=150,y = self.title_text_object.getY()-300)


      self.notes_file.drawCentredString(300, 800-300-self.title_text_object.getX()-50-150-50,"Video File Used : "+
                                        self.lesson_data_dictionary.get("Title_Video"))

      self.notes_file.showPage()



    def create_factual_notes(self):
      self.notes_file.setFont("Helvetica", 16)
      self.notes_file.drawCentredString(300, 820, "Terms and Definitions")
      i = 0
      while i < 3:
        factual_text_object = self.notes_file.beginText()
        factual_text_object.setTextOrigin(150,(700-i*210))
        factual_text_object.setHorizScale(60)
        factual_text_object.setFont("Helvetica", 16)
        factual_text_object.textLine(self.lesson_data_dictionary.get("Factual_Term"+str(i+1)))
        factual_text_object.setFont("Helvetica", 12)
        factual_text_object.textLines(self.lesson_data_dictionary.get("Factual_Term"+str(i+1)+"_Description"))
        self.notes_file.drawText(factual_text_object)

        self.notes_file.drawImage(self.lesson_root+os.path.sep+"images"+os.path.sep + self.lesson_data_dictionary.get("Factual_Image"+str(i+1)),
                                  width=200, height=200,
                                  x=factual_text_object.getX()+150, y=factual_text_object.getY()-100)
        i +=1

      self.notes_file.showPage()



    def create_application_notes(self):
      self.notes_file.setFont("Helvetica", 16)
      self.notes_file.drawCentredString(300, 820, "Skill Building")
      number_of_steps = int(self.lesson_data_dictionary.get("Application_Steps_Number"))
      i=0
      while i < number_of_steps:
        application_text_object = self.notes_file.beginText()
        application_text_object.setTextOrigin(100, (750 - i * 90))
        application_text_object.setHorizScale(70)
        application_text_object.setFont("Helvetica-Bold", 12)
        application_text_object.textLine(str(i+1)+". "+self.lesson_data_dictionary.get("Application_Step_Description_" + str(i + 1)))
        self.notes_file.drawText(application_text_object)
        if ( self.lesson_data_dictionary.get("Application_Steps_Widget_" + str(i + 1)) is not None):
               try:
                     self.notes_file.drawImage(self.lesson_root+os.path.sep+"images"+os.path.sep+ self.lesson_data_dictionary.get("Application_Steps_Widget_" + str(i + 1)),
                                  width=50, height=50,
                                  x=application_text_object.getX() + 50, y=application_text_object.getY() -40)
               except:
                   traceback.print_exc()

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
        assessment_text_object.setHorizScale(90)
        assessment_text_object.setFont("Helvetica", 12)
        assessment_text_object.textLines(assessment_text)
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
            self.notes_file.drawImage(
            self.lesson_root+os.path.sep+"saved_boards"+os.path.sep+file,
            width=500, height=500,
            x=50,y =150)
            file_index += 1
            self.notes_file.showPage()
        self.notes_file.save()

#if __name__ == "__main__":
    # dashboard_app = tk.Tk()
    # dashboard_app.configure(background="gray25")
    # dashboard_app.title("Learning Room Assessment")
    # dashboard_app.geometry("800x800")
    # frame = SnapshotView(dashboard_app)
    # # dashboard_app.rowconfigure(0,weight=1)
    # dashboard_app.columnconfigure(0, weight=1)
    # frame.grid(row=0, column=0)
    # dashboard_app.mainloop()