import logging
import os,lesson_list_PDF_notes
import shutil
import subprocess
import sys
import tkinter as tk
import traceback
from tkinter import messagebox, ttk, filedialog
import threading
from gtts import gTTS
from reportlab.pdfgen import canvas
from PIL import Image
from textwrap import wrap

import PDF_Utils
import data_capture_notes

logger = logging.getLogger("MagicLogger")

file_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
db = file_root + os.path.sep + "MagicRoom.db"

class SnapshotView(tk.Toplevel):
    def __init__(self,parent,lesson_id="",filename="",*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        s = ttk.Style(self)
        self.lesson_text_full = ""
        s.theme_use("clam")

        s.configure('Notes.TLabelframe', background='gray27')
        s.configure('Notes.TLabelframe.Label', font=('helvetica', 14, 'bold'))
        s.configure('Notes.TLabelframe.Label', background='gray27', foreground='white')

        self.configure(background="gray25")
        self.file_root = file_root
        self.lesson_id = lesson_id
        self.view_flag = 0
        if lesson_id =="" or lesson_id is None:
            app = lesson_list_PDF_notes.MagicLessonList(parent=self)
            app.geometry("340x700+50+50")
            self.wait_window(app)
            print(self.selected_lessons)
            self.lesson_id = self.selected_lessons[0]
            self.view_flag=1

            filename = self.file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(self.lesson_id)+os.path.sep+"notes_"+str(self.lesson_id)+".pdf"

        if self.view_flag == 1:
            self.rowconfigure(0,weight=1)
            self.columnconfigure(0, weight=1)
            self.notes_labelframe = ttk.Labelframe(self, text="Generate Lesson Notes", style="Notes.TLabelframe")
            self.notes_PDF_label = ttk.Label(self.notes_labelframe, text="View Notes",
                                                  style="Notes.TLabelframe.Label")
            self.notes_condition_label = ttk.Label(self, text="Audio notes generation requires internet connectivity"
                                            ,background="gray27",foreground="aquamarine", font=("helvetica",10,"bold"))
            self.notes_PDF_Button = ttk.Button(self.notes_labelframe, text="View",
                                                    command=lambda: self.display_PDF(filename), style="Blue.TButton")
            self.save_file_button = ttk.Button(self.notes_labelframe, text="Save",
                                               command=lambda: self.save_notes_file(filename,
                                                                                         self.lesson_id),
                                               style="Blue.TButton")
            self.notes_audio_label = ttk.Label(self.notes_labelframe, text="Generate Audio Notes",
                                             style="Notes.TLabelframe.Label")
            self.notes_audio_Button = ttk.Button(self.notes_labelframe, text="Generate",
                                               command=lambda: self.generate_notes_audio(self.lesson_id), style="Blue.TButton")
            filename_audio = self.file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                self.lesson_id) + os.path.sep + "audio_notes_" + str(self.lesson_id) + ".mp3"
            self.save_audio_button = ttk.Button(self.notes_labelframe, text="Save",
                                               command=lambda: self.save_notes_audio(filename_audio,
                                                                                    self.lesson_id),
                                               style="Blue.TButton")

            if (os.path.exists(filename_audio)):
                self.audio_play_label = ttk.Label(self.notes_labelframe, text="Play Existing Audio Notes",
                                                  style="Notes.TLabelframe.Label")
                self.audio_play_button = ttk.Button(self.notes_labelframe, text="Play",
                                                    command=lambda: self.play_notes_audio(self.lesson_id),
                                                    style="Blue.TButton")
                self.audio_play_label.grid(padx=5,row=2, column=0,sticky=tk.W)
                self.audio_play_button.grid(row=2, column=1)

            self.notes_PDF_label.grid(row=0, column=0,padx=5,pady=5,sticky=tk.W)
            self.notes_PDF_Button.grid(row=0, column=1,padx=5,pady=5)
            self.save_file_button.grid(row=0, column=2,padx=5,pady=5)

            self.notes_audio_label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.W)
            self.notes_audio_Button.grid(row=1, column=1, padx=5, pady=5)
            self.save_audio_button.grid(row=1, column=2, padx=5, pady=5)

            self.notes_labelframe.grid(row=0,column=0,padx=5,pady=5)
            self.notes_condition_label.grid(row=2,column=0)
            pdf_data = PDF_Utils.PDFUtils(self.lesson_id,filename)


            self.lesson_text_full = pdf_data.lesson_text_full



    def display_PDF(self,notes_file):
        try:
            if sys.platform == "win32":
                os.startfile(notes_file)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, notes_file])
        except:
            messagebox.showerror("File open Error",
                                 "File could not be opened. Check if you have Adobe Reader Installed or if the folder has full permissions")

    def save_notes_file(self, notes_file, lesson_id):
        try:
            filename = filedialog.askdirectory(parent=self)
            shutil.copyfile(notes_file, filename + os.path.sep + "notes" + str(lesson_id) + ".pdf")
            messagebox.showinfo("Copy Message", "File Copied",parent=self)
        except:
            messagebox.showwarning("File Save Error", "File could not be copied", parent=self)
            print(traceback.print_exc())

    def save_notes_audio(self, notes_audio_file, lesson_id):
        try:
            filename = filedialog.askdirectory(parent=self)
            shutil.copyfile(notes_audio_file, filename + os.path.sep + "audio_notes" + str(lesson_id) + ".mp3")
            messagebox.showinfo("Copy Message", "File Copied",parent=self)
        except:
            messagebox.showwarning("File Save Error", "File could not be copied", parent=self)
            print(traceback.print_exc())

    def generate_notes_audio(self,lesson_id):
        audio_generate = threading.Thread(target=self.generate_audio, args=(lesson_id,))
        audio_generate.start()
        messagebox.showinfo("Staus", "Online audio generation triggered.\n Player will start once generation is complete",parent=self)
        audio_generate.join(20)
        if sys.platform == "win32":
            os.startfile(file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(lesson_id)+os.path.sep+"audio_notes_"+str(lesson_id)+".mp3")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(lesson_id)+os.path.sep+"audio_notes_"+str(lesson_id)+".mp3"
        ])

    def generate_audio(self, lesson_id):
        try:

            audio_object = gTTS(text=self.lesson_text_full, lang="en", slow=False)
            filepath = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                lesson_id) + os.path.sep + "audio_notes_" + str(lesson_id) + ".mp3"
            print(filepath)
            audio_object.save(filepath)
        except:
            messagebox.showerror("Audio File Error", "Could not generate the audio file",parent=self)
            print("could not generate the audio file")
            logger.exception("Could not generate the audio file")

    def play_notes_audio(self, lesson_id):

        try:

            if sys.platform == "win32":
                os.startfile(file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                    lesson_id) + os.path.sep + "audio_notes_" + str(lesson_id) + ".mp3")
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                    lesson_id) + os.path.sep + "audio_notes_" + str(lesson_id) + ".mp3"
                                 ])
        except:
            messagebox.showerror("Play Error", "Could not play the audio file",parent=self)
            print("could not play the audio file")
            logger.exception("Could not play the audio file")


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
