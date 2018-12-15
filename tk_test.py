#-*- coding: utf-8 -*-
from tkinter import *

#main class for for frame taht will be always open and in which we will see all the pages
class Window(Tk):

	def __init__(self):
		#creates container for all pages
		Tk.__init__(self)
		container = Frame(self)
		container.pack(side="top", fill="both", expand = "True")

		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)
		#creates dictionary for list of all pages
		self.frames = {}

		frame = StartPage(container,self)
		self.frames[StartPage] = frame

		frame.grid(row=0, column=0,sticky='nsew')

		self.show_frame(StartPage)

	def show_frame(self,cont):

		frame = self.frames[cont]
		frame.tkraise()

#code of the actual page/window
class StartPage(Frame):
	def __init__(self,parent,controller):
		Frame .__init__(self,parent)

		label = Label(text='Hello')
		label.pack(pady=10,padx=10)

app = Window()
app.mainloop()