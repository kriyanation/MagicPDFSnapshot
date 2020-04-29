from reportlab.pdfgen import canvas
import json
import cv2
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

image_root = "/home/ram/Rams/GameDev/images/"
video_root = "/home/ram/Rams/GameDev/videos/"

class SnapshotView():
    def __init__(self,jsondata):
        self.lesson_data_dictionary = json.loads(jsondata)[0]
        self.notes_file = canvas.Canvas(str(self.lesson_data_dictionary.get("Lesson_ID")) + ".pdf")

    def create_title_notes(self):
      self.Title_Font = self.notes_file.setFont("Helvetica", 16)
      self.notes_file.drawCentredString(300, 820, self.lesson_data_dictionary.get("Lesson_Title"))
      self.Text_Font = self.notes_file.setFont("Helvetica", 12)
      self.title_text_object = self.notes_file.beginText()
      self.title_text_object.setTextOrigin(50,800)
      self.title_text_object.setHorizScale(90)
      self.title_text_object.textLines(self.lesson_data_dictionary.get("Title_Running_Notes"))
      self.notes_file.drawText(self.title_text_object)
      self.notes_file.drawImage(image_root+self.lesson_data_dictionary.get("Title_Image"),width=300,height=300,x=150,y = self.title_text_object.getY()-300)
      vidcap = cv2.VideoCapture(video_root+self.lesson_data_dictionary.get("Title_Video"))
      i=0
      while vidcap.isOpened():
        success, image = vidcap.read()
        if success and i==50:
          cv2.imwrite("frame.jpg", image)  # save frame as JPEG file
          break;
        i+=1

      self.notes_file.drawImage("frame.jpg", width=300, height=150,x=150,y=self.title_text_object.getY()-500)
      vidcap.release()
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

        self.notes_file.drawImage(image_root + self.lesson_data_dictionary.get("Factual_Image"+str(i+1)),
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
        self.notes_file.drawImage(image_root + self.lesson_data_dictionary.get("Application_Steps_Widget_" + str(i + 1)),
                                  width=50, height=50,
                                  x=application_text_object.getX() + 50, y=application_text_object.getY() -40)
        i += 1
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
        self.notes_file.save()