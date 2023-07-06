import customtkinter as ctk 
import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog,Canvas
from settings import *

class Panel(ctk.CTkFrame):
	def __init__(self,parent):
		super().__init__(parent,fg_color=DARK_GREY)
		self.pack(fill='x',pady=4,ipady=8)
		#ctk.CTkSlider(self).pack()

class SliderPanel(Panel):
	def __init__(self,parent,text,data_var,minv,maxv):
		super().__init__(parent=parent)

		self.data_var=data_var
		self.data_var.trace('w',self.updatetext)
		self.columnconfigure((0,1),weight=1)
		self.rowconfigure((0,1),weight=1)
		ctk.CTkLabel(self,text=text).grid(column=0,row=0,pady=5,sticky='w',padx=5)
		self.valuetext=ctk.CTkLabel(self,text=0)
		self.valuetext.grid(column=1,row=0,sticky='e',padx=5)
		ctk.CTkSlider(self,variable=self.data_var,from_=minv,to=maxv).grid(column=0,row=1,columnspan=2,sticky='ew',padx=5)
	
	def updatetext(self,*args):
		self.valuetext.configure(text=f'{round(self.data_var.get(),2)}')



class SegmentPanel(Panel):
	def __init__(self,parent,text,data_var,options):
		super().__init__(parent)
		ctk.CTkLabel(self,text=text).pack()
		ctk.CTkSegmentedButton(self,variable=data_var,values=options).pack(expand=True,fill='both',padx=5,pady=5)
class SwitchPanel(Panel):
	def __init__(self,parent,*switches):
		super().__init__(parent)
		for var,text in switches:
			switch=ctk.CTkSwitch(self,text=text,variable=var,button_color = BLUE,fg_color=SLIDER_BG)
			switch.pack(side='left',expand=True,fill='both',padx=5,pady=5)


class DropDownPanel(ctk.CTkOptionMenu):
	def __init__(self,parent,data_var,options):
		super().__init__(parent,values=options,variable=data_var,fg_color=DARK_GREY,command=lambda event:print(data_var.get()))
		self.pack(pady=5,fill='x')

class RevertButton(ctk.CTkButton):
	def __init__(self,parent,*args):
		super().__init__(parent,text='Revert',command=self.reset)
		self.pack(side='bottom',pady=15)
		self.args=args
	def reset(self):
		for var,default in self.args:
			var.set(default)


class FileNamePanel(Panel):
	def __init__(self,parent,name_string,file_string):
		super().__init__(parent)
		self.name_string=name_string
		self.name_string.trace('w',self.update_text)
		self.file_string=file_string
		ctk.CTkEntry(self,textvariable=self.name_string).pack(fill='x',padx=20,pady=5)
		framebox=ctk.CTkFrame(self,fg_color='transparent')
		jpgcheck=ctk.CTkCheckBox(framebox,text='jpg',variable=self.file_string,onvalue='jpg',offvalue='png',command= lambda:self.clicked('jpg'))
		pngcheck=ctk.CTkCheckBox(framebox,text='png',variable=self.file_string,onvalue='png',offvalue='jpg',command= lambda:self.clicked('png'))	
		framebox.pack(expand=True,fill='x',padx=15)
		jpgcheck.pack(side='left',fill='x',expand=True)
		pngcheck.pack(side='left',fill='x',expand=True)


		self.output=ctk.CTkLabel(self,text=' ')
		self.output.pack()

	def update_text(self,*args):
		if self.name_string.get():
			text=self.name_string.get().replace(' ','_') + '.'+ self.file_string.get()
			self.output.configure(text=text)

	def clicked(self,type): 
		self.file_string.set(type)
		self.update_text()


class FilePath(Panel):
	def __init__(self,parent,name,file,pathstring):
		super().__init__(parent)
		self.pathstring=pathstring
		self.name=name 
		self.file=file
		ctk.CTkButton(self,text='open directory',command=self.output).pack(pady=5)
		ctk.CTkEntry(self,textvariable=self.pathstring).pack(expand=True,fill='both',padx=5,pady=5)
	
	def output(self):
		self.path=self.name.get().replace(' ','_') + '.'+ self.file.get()
		self.pathstring.set(filedialog.askdirectory())
		



class SaveButton(ctk.CTkButton):
	def __init__(self,parent,export_image,name,file,path):
		super().__init__(parent,text='save',command=self.save)

		self.export_image=export_image
		self.name=name
		self.file=file
		self.path=path 
	def save(self):
		self.export_image(self.name.get(),self.file.get(),self.path.get())
		#print(self.name.get(),self.file.get(),self.path.get())