import customtkinter as ctk 
from options import *


class Menu(ctk.CTkTabview):
	def __init__(self,parent,pos_vars,colour_vars,effect_vars,export_image):
		super().__init__(parent)
		self.grid(row=0,column=0,sticky='nsew',padx=5)

		
		self.add('Position')
		self.add('Colour')
		self.add('Effects')
		self.add('Export')

		#frames
		PositionFrame(self.tab('Position'),pos_vars)
		ColourFrame(self.tab('Colour'),colour_vars)
		EffectFrame(self.tab('Effects'),effect_vars)
		ExportFrame(self.tab('Export'),export_image)

class PositionFrame(ctk.CTkFrame):
	def __init__(self,parent,pos_vars):
		super().__init__(parent)
		self.pack(expand=True,fill='both')
		SliderPanel(self,'Rotation',pos_vars['rotate'],0,360)
		SliderPanel(self,'Zoom',pos_vars['zoom'],0,200)
		SegmentPanel(self,'Inverse',pos_vars['flip'],FLIP_OPTIONS)
		RevertButton(self,(pos_vars['rotate'],ROTATE_DEFAULT),(pos_vars['zoom'],ZOOM_DEFAULT),(pos_vars['flip'],FLIP_OPTIONS[0]))
class ColourFrame(ctk.CTkFrame):
	def __init__(self,parent,colour_vars):
		super().__init__(parent)
		self.pack(expand=True,fill='both')
		SwitchPanel(self,(colour_vars['greyscale'],'black/white'),(colour_vars['invert'],'Invert'))
		SliderPanel(self,'Brightness',colour_vars['brightness'],0,10)
		SliderPanel(self,'Vibrance',colour_vars['vibrance'],0,5)
		RevertButton(self,
			(colour_vars['brightness'],BRIGHTNESS_DEFAULT),(colour_vars['greyscale'],GRAYSCALE_DEFAULT),(colour_vars['invert'],INVERT_DEFAULT),
			(colour_vars['vibrance'],VIBRANCE_DEFAULT))

class EffectFrame(ctk.CTkFrame):
	def __init__(self,parent,effect_vars):
		super().__init__(parent)
		self.pack(expand=True,fill='both')
		SliderPanel(self,'Blur',effect_vars['blur'],0,10)
		SliderPanel(self,'Contrast',effect_vars['contrast'],0,10)
		DropDownPanel(self,effect_vars['effect'], EFFECT_OPTIONS)
		RevertButton(self,
			(effect_vars['blur'],BLUR_DEFAULT),(effect_vars['contrast'],CONTRAST_DEFAULT),(effect_vars['effect'],EFFECT_OPTIONS[0]))


class ExportFrame(ctk.CTkFrame):
	def __init__(self,parent,export_image):
		super().__init__(parent)
		self.pack(expand=True,fill='both')
		
		self.name_string=ctk.StringVar()
		self.file_string=ctk.StringVar(value='jpg')
		self.path_string=ctk.StringVar()
		
		FileNamePanel(self,self.name_string,self.file_string)
		FilePath(self,self.name_string,self.file_string,self.path_string)
		SaveButton(self,export_image,self.name_string,self.file_string,self.path_string).pack(side='bottom',pady=5)