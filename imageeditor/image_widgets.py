import customtkinter as ctk 
from tkinter import filedialog,Canvas
from settings import *
class ImageImport(ctk.CTkFrame):
	def __init__(self,parent,import_func):
		super().__init__(parent)
		self.pack(expand=True,fill='both')
		self.import_func=import_func
		self.button=ctk.CTkButton(self,text='open image',command=self.open_dialog)
		self.button.pack(expand=True)


	def open_dialog(self):
		path=filedialog.askopenfile().name
		self.import_func(path)

class ImageOutput(Canvas):
	def __init__(self,parent,resize_image):
		super().__init__(parent,background=BACKGROUND_COLOUR,bd=0,highlightthickness=0,relief='ridge')
		self.grid(row=0,column=1,sticky='nsew',pady=40,padx=10)
		self.bind('<Configure>',resize_image)

class CloseOutput(ctk.CTkButton):
	def __init__(self,parent,close_func):
		super().__init__(parent,text='x',fg_color='red',width=40,height=40,text_color=WHITE,hover_color=CLOSE_RED,command= close_func)
		self.place(relx=0.99,rely=0.01,anchor='ne')


