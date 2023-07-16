import customtkinter as ctk 
from image_widgets import *
from menu import *
from PIL import Image,ImageEnhance,ImageTk,ImageFilter,ImageOps
from settings import *
from options import ThemeDropDownPanel


class App(ctk.CTk):
	def __init__(self,theme,colourmode,themename):
		print(colourmode,theme)
		super().__init__()
		ctk.set_appearance_mode(f'{colourmode}')
		#ctk.set_default_color_theme('pinktheme.json')
		#ctk.set_appearance_mode									_default_color_theme('green')
		#ctk.set_appearance_mode('light')
		#ctk.set_appearance_mode('blue')
		ctk.set_default_color_theme(f'{theme}')
		self.themename=themename
		self.geometry('1000x600')
		self.title('Aidans Photo editor')
		self.minsize(900,500)
		self.iconbitmap("icons.ico")

		#layout
		self.rowconfigure(0,weight=1)
		self.columnconfigure(0,weight=2,uniform='a')
		self.columnconfigure(1,weight=6,uniform='a')
		self.init_parameters()

		#canvas data
		self.image_width=0
		self.image_height=0
		self.canvas_width=0
		self.canvas_height=0

		#self.bind('<Configure>',lambda event:print(event))
		#widgets
		self.image_import=ImageImport(self,self.import_image)

		#import button


		#run
		self.mainloop()


	def init_parameters(self):
		self.pos_vars={'rotate':ctk.DoubleVar(value=ROTATE_DEFAULT	),
		'zoom':ctk.DoubleVar(value=ZOOM_DEFAULT),
		'flip':ctk.StringVar(value=FLIP_OPTIONS[0])}
		

		self.colour_vars={'brightness':ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
		'greyscale':ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
		'invert':ctk.BooleanVar(value=INVERT_DEFAULT),
		'vibrance':ctk.DoubleVar(value=VIBRANCE_DEFAULT)}
		
		self.effect_vars={'blur':ctk.DoubleVar(value=BLUR_DEFAULT	),
		'contrast':ctk.IntVar(value=CONTRAST_DEFAULT),
		'effect':ctk.StringVar(value=EFFECT_OPTIONS[0])}		

		self.all_vars= self.pos_vars | self.colour_vars | self.effect_vars
		
		for var in self.all_vars.values():
			var.trace('w',self.manipulate_image)

		

	def manipulate_image(self,*args):
		self.image=self.original

		self.image=self.image.rotate(self.pos_vars['rotate'].get())
		

		self.image= ImageOps.crop(image=self.image,border=self.pos_vars['zoom'].get())





		if self.pos_vars['flip'].get()=='X':
			self.image=ImageOps.mirror(self.image)
		if self.pos_vars['flip'].get()=='Y':
			self.image=ImageOps.flip(self.image)
		if self.pos_vars['flip'].get()=='Both':
			self.image=ImageOps.flip(self.image)
			self.image=ImageOps.mirror(self.image)


		brightenhance=ImageEnhance.Brightness(self.image)
		self.image=brightenhance.enhance(self.colour_vars['brightness'].get())			

		vibrenhance=ImageEnhance.Color(self.image)
		self.image=vibrenhance.enhance(self.colour_vars['vibrance'].get())

		if self.colour_vars['greyscale'].get():
			self.image=ImageOps.grayscale(self.image)

		if self.colour_vars['invert'].get():
			self.image=ImageOps.invert(self.image)


		self.image=self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))
		self.image=self.image.filter(ImageFilter.UnsharpMask(self.effect_vars['contrast'].get()))


		if self.effect_vars['effect'].get()=='Emboss': 
			self.image=self.image.filter(ImageFilter.EMBOSS)
		if self.effect_vars['effect'].get()=='Find edges': 
			self.image=self.image.filter(ImageFilter.FIND_EDGES)
		if self.effect_vars['effect'].get()=='Contour': 
			self.image=self.image.filter(ImageFilter.CONTOUR)
		if self.effect_vars['effect'].get()=='Edge enhance': 
			self.image=self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)

		self.place_image()
		
	def import_image(self,path):
		self.original=Image.open(path)
		self.image=self.original
		self.image_ratio=self.image.size[0]/self.image.size[1]
		self.image_tk=ImageTk.PhotoImage(self.image)
		self.image_import.pack_forget()
		self.image_output=ImageOutput(self,self.resize_image)
		self.close_button=CloseOutput(self,self.close_image)
		self.menu=Menu(self,self.pos_vars,self.colour_vars,self.effect_vars,self.export_image,self.themename)



	def close_image(self):
		self.image_output.grid_forget()
		self.menu.grid_forget()
		self.image_import=ImageImport(self,self.import_image)

	def resize_image(self,event):


		self.canvas_width=event.width
		self.canvas_height=event.height

		if event.width>event.height:
			self.image_height=int(event.height)
			self.image_width=int(self.image_ratio*self.image_height)
		else:
			self.image_width=int(event.width)
			self.image_height=int(self.image_width/self.image_ratio)
		self.place_image()

	def place_image(self):
		self.resized_image=self.image.resize((self.image_width,self.image_height))
		self.resized_tk=ImageTk.PhotoImage(self.resized_image)
		self.image_output.delete('all')
		self.image_output.create_image(int(self.canvas_width )/2,int(self.canvas_height)/2,anchor='center',image=self.resized_tk)

	def export_image(self,name,file,path):
		exportstring=f'{path}/{name}.{file}'
		print(f'export string:',exportstring)
		self.image.save(exportstring)





class ThemeSelector(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.geometry('400x400')
		self.title('theme selector')
		self.minsize(400,400)
		self.iconbitmap("icons.ico")
		self.configure(background='pink')
		self.themename=ctk.StringVar(value='blue')
		self.themeselector=ThemeDropDownPanel(self,self.themename,['blue','green',
			'pink','red','purple','black'])
		okbutton=ctk.CTkButton(self,text='confirm',command=self.themeconfirm)
		okbutton.pack(expand=True)

		#run
		self.mainloop()

	def themeconfirm(self):
		themedict={'blue':('blue','dark'),
		'green':('green','light'),
		'pink':('themes/pinktheme.json','light'),
		'red':('themes/red.json','light'),
		'purple':('themes/purple.json','light'),
		'black':('themes/black.json','light')}



		self.destroy()
		App(themedict[self.themename.get()][0],themedict[self.themename.get()][1],self.themename.get())


ThemeSelector()
#App()