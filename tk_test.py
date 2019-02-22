#-*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3 as sql
import datetime


class DateFunctions:

	def DateFormat(number):


		if int(number) < 10:
			return "0" + str(number)
		return number

	if (int(datetime.datetime.date(datetime.datetime.now()).month)<10):

		CurrentYearMonth = str(datetime.datetime.date(datetime.datetime.now()).year) + '-0' + str(
		datetime.datetime.date(datetime.datetime.now()).month)
	else:
		CurrentYearMonth = str(datetime.datetime.date(datetime.datetime.now()).year) + '-' + str(
		datetime.datetime.date(datetime.datetime.now()).month)


	CurrentDate = str(datetime.datetime.date(datetime.datetime.now()).year) + '-' + DateFormat(str(
	datetime.datetime.date(datetime.datetime.now()).month)) + '-' + DateFormat(str(
		datetime.datetime.date(datetime.datetime.now()).day))

#main class for for frame taht will be always open and in which we will see all the pages
class Window(Tk):

	def __init__(self):
		global DB
		DB=Database()

		#creates container for all pages
		Tk.__init__(self)
		container = Frame(self)
		container.pack(side="top", fill="both", expand = "True")

		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)

		menubar = MenuBar(container)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label='save settings',)
		self.config(menu=menubar)



		#creates dictionary for list of all pages
		self.frames = {}
		#creates the pages from the dictionary
		for F in (StartPage, MainPage, ViewPage): #AddPage
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0,sticky='nsew')

		self.show_frame(StartPage)

	def show_frame(self,cont):

		frame = self.frames[cont]
		frame.update_idletasks()
		frame.tkraise()


class MenuBar(Menu):

	def __init__(self,parent):
		Menu.__init__(self,parent)



		self.add_command(label='Main', command = lambda: app.show_frame(MainPage))
		#self.add_command(label='Add', command = lambda: app.show_frame(AddPage))
		self.add_command(label='View', command = lambda: app.show_frame(ViewPage))
		self.add_command(label='Savings', command = lambda: app.show_frame(MainPage))
		self.add_command(label='Forecast', command = lambda: app.show_frame(MainPage))
		self.add_command(label='Instruments', command = lambda: app.show_frame(MainPage))

		GraphsMenu = Menu(self, tearoff=False)
		self.add_cascade(label='Graphs', underline=0,menu=GraphsMenu)
		GraphsMenu.add_command(label='Incomes', command = lambda: app.show_frame(MainPage))
		GraphsMenu.add_command(label='Expenditures', command = lambda: app.show_frame(MainPage))
		GraphsMenu.add_command(label='Savings', command = lambda: app.show_frame(MainPage))

#code of the actual page/window
class StartPage(Frame):
	def __init__(self,parent,controller):
		Frame .__init__(self,parent)

		MainPage_Button = ttk.Button(self, text='Main Page', command = lambda: controller.show_frame(MainPage)) # lamdbada to avoid auto starting functions
		MainPage_Button.pack(pady=10,padx=10)

class MainPage(Frame):



	def __init__(self,parent,controller):
			Frame .__init__(self,parent)



			names = ['eKonto','Cash','eMax','Retirement','Target','Emergency','Fun']
			Przychody = ['Wynagrodzenie', 'Przychody z kapitalu', 'Inne przychody']
			Rozchody = ['Zywnosc', 'Transport', 'Odziez', 'Telefon', 'Higiena', 'Zdrowie', 'Edukacja', 'Rekreacja', 'Uzywki',
			'Dary', 'Inne', 'Oplaty', 'Srodki trwale', 'Mieszkanie', 'Oplaty mieszkanie', 'Wspolne']

			global RozchodyVariables, PrzychodyVariables, namesVariables,MonthEntry2
			RozchodyVariables = {}
			PrzychodyVariables = {}
			namesVariables = {}

			YearMonth=DateFunctions.CurrentYearMonth
			MonthLabel = Label(self,text='Month')
			MonthLabel.grid(row=0,column=0)

			MonthEntryVariable = StringVar()
			MonthEntryVariable .set(DateFunctions.CurrentYearMonth)


			MonthEntry = Entry(self,textvariable = MonthEntryVariable)
			MonthEntry.grid(row=0,column=1)
			MonthEntry2 = MonthEntry

			###creates the labels for accounts
			i=2
			for name in names:
				LabelName = Label(self,text=name)
				LabelName.grid(row=i, column=0)

				Value=StringVar()
				Value.set(DB.GetValue(name))

				LabelValue = Label(self,textvariable=Value)
				LabelValue.grid(row=i,column=1)

				i=i+1
			#############
			##PRZYCHODY##
			#############
			i=i+2
			for name in Przychody:
				LabelName = Label(self,text=name)
				LabelName.grid(row=i, column=0)

				#PrzychodyVariables[name] = DB.GetAmount(name,MonthEntryVariable.get())
				PrzychodyVariables[name]=StringVar()
				PrzychodyVariables[name].set(DB.GetAmount(name,MonthEntryVariable.get()))

				LabelValue = Label(self,textvariable = PrzychodyVariables[name])
				LabelValue.grid(row=i,column=1)

				i=i+1

			############
			##ROZCHODY##
			############
			i=i-len(Przychody)
			for name in Rozchody:
				LabelName = Label(self,text=name)
				LabelName.grid(row=i, column=3)


				RozchodyVariables[i] = DB.GetAmount(name,MonthEntryVariable.get())
				Value=StringVar()
				Value.set(RozchodyVariables[i])

				LabelValue = Label(self,textvariable=Value)
				LabelValue.grid(row=i,column=4)



				i=i+1


			RefreshButton = Button(self,text = 'Refresh', command = lambda: DB.Refresh(str(MonthEntry2.get())))
			RefreshButton.grid(row = 0, column =2)
			global ValueTest
			ValueTest=StringVar()
			ValueTest.set(DB.GetAmount('Wynagrodzenie',MonthEntryVariable.get()))

			LabelValueTest= Label(self,textvariable=ValueTest)
			LabelValueTest.grid(row=7,column=7)

			extrabutton = Button(self,text='add',command = lambda: self.adding())
			extrabutton.grid(row =3, column=5)

	def adding(self):

		popup = tk.Tk()

		Przychody = ['Wynagrodzenie', 'Przychody z kapitalu', 'Inne przychody']

		Rozchody = ['Zywnosc', 'Transport', 'Odziez', 'Telefon', 'Higiena', 'Zdrowie', 'Edukacja', 'Rekreacja', 'Uzywki',
		'Dary', 'Inne', 'Oplaty', 'Srodki trwale', 'Mieszkanie', 'Oplaty mieszkanie', 'Wspolne']

		Transfer = ['Cash-->eKonto', 'eKonto-->eMax plus-Emerytura', 'eKonto-->eMax plus-Cel dlugo-dystansowy',
		'eKonto-->eMax-Emergency',
		'eKonto-->eMax-Fundusz rozrywkowy', 'eKonto-->Cash', 'eKonto-->Obligacje-Emerytura',
		'eKonto-->Obligacje-Cel dlugo-dystansowy',
		'eMax plus- Emerytura-->eKonto', 'eMax plus-Cel dlugo-dystansowy-->eKonto', 'eMax-Emergency-->eKonto',
		'eMax-Fundusz rozrywkowy-->eKonto',
		'Skarbonka -->Gotówka', 'Obligacje-Emerytura-->eKonto', 'Obligacje-Cel dlugo-dystansowy-->eKonto']

		Types = ('Przychody', 'Rozchody', 'Transfer')

		Payments = ('eKonto', 'Cash', 'eMax plus-Emerytura', 'eMax plus-Cel dlugo-dystansowy', 'eMax-Emergency', 'eMax-Fundusz rozrywkowy')

		Amounts = []


		global Type, Category, OptionCategory, OptionPayment
		def set_options(*args):


			if Type.get() == '(default)':
				return None

			# refresh Category
			Category.set('(select)')
			OptionCategory['menu'].delete(0, 'end')

			# pick new set of options

			if Type.get() == 'Przychody':
				new_options = Przychody
				#print('przychody')
			elif Type.get() == 'Rozchody':
				new_options = Rozchody
			else:
				new_options = []

			# add new options in
			for item in new_options:
				OptionCategory['menu'].add_command(label=item, command=tk._setit(Category, item))

			Payment.set('eKonto')
			OptionPayment['menu'].delete(0, 'end')

			if Type.get() == 'Transfer':
				new_options2 = Transfer
			else:
				new_options2 = Payments

			for item in new_options2:
				OptionPayment['menu'].add_command(label=item, command=tk._setit(Payment, item))


		Labels=['Date','Type','Category','Amount','Payment']
		i=0
		for name in Labels:
			LabelName = Label(popup,text=name)
			LabelName.grid(row=i, column=0)
			i=i+1

		global EntryDateVariable,EntryAmount, Payment

		#fills the date entry with current date, varaiable is created based on popup object
		EntryDateVariable = StringVar(popup)
		EntryDateVariable .set(DateFunctions.CurrentDate)

		EntryDate = Entry(popup,textvariable=EntryDateVariable)
		EntryDate.grid(row=0,column=1)

		Type = StringVar()
		Type.set('Rozchody')

		LabelType = Label(popup,text='Type')
		LabelType.grid(row=1, column=0)

		OptionType = OptionMenu(popup, Type, *Types)
		OptionType.grid(row=1, column=1)

		# trace varaible and change drop down
		Type.trace('w', set_options)

		Category = StringVar()
		Category.set('Zywnosc')

		LabelCategory = Label(popup,text='Category')
		LabelCategory.grid(row=2, column=0)

		OptionCategory = OptionMenu(popup, Category, 'Zywnosc')
		OptionCategory.grid(row=2, column=1)

		EntryAmount = Entry(popup,width=9)
		EntryAmount.grid(row=3, column=1)


		Payment = StringVar()
		Payment.set('eKonto')

		OptionPayment = OptionMenu(popup, Payment, *Payments)
		OptionPayment.grid(row=4, column=1)

		AddButton = Button(popup,text='Add', command=lambda: DB.Add())
		AddButton.grid(row=5, column=1)


		def DestroyPopup():
			popup.destroy()

		popup.mainloop()

# class AddPage(Frame):
#
#
#
# 	def __init__(self,parent,controller):
# 			Frame .__init__(self,parent)
#
#
# 			Przychody = ['Wynagrodzenie', 'Przychody z kapitalu', 'Inne przychody']
# 			Rozchody = ['Zywnosc', 'Transport', 'Odziez', 'Telefon', 'Higiena', 'Zdrowie', 'Edukacja', 'Rekreacja', 'Uzywki',
# 			'Dary', 'Inne', 'Oplaty', 'Srodki trwale', 'Mieszkanie', 'Oplaty mieszkanie', 'Wspolne']
# 			Transfer = ['Cash-->eKonto', 'eKonto-->eMax plus-Emerytura', 'eKonto-->eMax plus-Cel dlugo-dystansowy',
# 			'eKonto-->eMax-Emergency',
# 			'eKonto-->eMax-Fundusz rozrywkowy', 'eKonto-->Cash', 'eKonto-->Obligacje-Emerytura',
# 			'eKonto-->Obligacje-Cel dlugo-dystansowy',
# 			'eMax plus- Emerytura-->eKonto', 'eMax plus-Cel dlugo-dystansowy-->eKonto', 'eMax-Emergency-->eKonto',
# 			'eMax-Fundusz rozrywkowy-->eKonto',
# 			'Skarbonka -->Gotówka', 'Obligacje-Emerytura-->eKonto', 'Obligacje-Cel dlugo-dystansowy-->eKonto']
#
# 			Types = ('Przychody', 'Rozchody', 'Transfer')
# 			Payments = (
# 			'eKonto', 'Cash', 'eMax plus-Emerytura', 'eMax plus-Cel dlugo-dystansowy', 'eMax-Emergency', 'eMax-Fundusz rozrywkowy')
# 			Amounts = []
#
#
# 			global Type, Category, OptionCategory, OptionPayment
# 			def set_options(*args):
#
#
# 				if Type.get() == '(default)':
# 					return None
#
# 				# refresh Category
# 				Category.set('(select)')
# 				OptionCategory['menu'].delete(0, 'end')
#
# 				# pick new set of options
#
# 				if Type.get() == 'Przychody':
# 					new_options = Przychody
# 					#print('przychody')
# 				elif Type.get() == 'Rozchody':
# 					new_options = Rozchody
# 				else:
# 					new_options = []
#
# 				# add new options in
# 				for item in new_options:
# 					OptionCategory['menu'].add_command(label=item, command=tk._setit(Category, item))
#
# 				Payment.set('eKonto')
# 				OptionPayment['menu'].delete(0, 'end')
#
# 				if Type.get() == 'Transfer':
# 					new_options2 = Transfer
# 				else:
# 					new_options2 = Payments
#
# 				for item in new_options2:
# 					OptionPayment['menu'].add_command(label=item, command=tk._setit(Payment, item))
#
#
# 			Labels=['Date','Type','Category','Amount','Payment']
# 			i=0
# 			for name in Labels:
# 				LabelName = Label(self,text=name)
# 				LabelName.grid(row=i, column=0)
# 				i=i+1
# 			global EntryDateVariable,EntryAmount, Payment
# 			EntryDateVariable = StringVar()
# 			EntryDateVariable .set(DateFunctions.CurrentDate)
#
# 			EntryDate = Entry(self,textvariable=EntryDateVariable)
# 			EntryDate.grid(row=0,column=1)
#
# 			Type = StringVar()
# 			Type.set('Rozchody')
#
# 			LabelType = Label(self,text='Type')
# 			LabelType.grid(row=1, column=0)
#
# 			OptionType = OptionMenu(self, Type, *Types)
# 			OptionType.grid(row=1, column=1)
#
# 			# trace varaible and change drop down
# 			Type.trace('w', set_options)
#
# 			Category = StringVar()
# 			Category.set('Zywnosc')
#
# 			LabelCategory = Label(self,text='Category')
# 			LabelCategory.grid(row=2, column=0)
#
# 			OptionCategory = OptionMenu(self, Category, 'Zywnosc')
# 			OptionCategory.grid(row=2, column=1)
#
# 			EntryAmount = Entry(self,width=9)
# 			EntryAmount.grid(row=3, column=1)
#
#
# 			Payment = StringVar()
# 			Payment.set('eKonto')
#
# 			OptionPayment = OptionMenu(self, Payment, *Payments)
# 			OptionPayment.grid(row=4, column=1)
#
# 			AddButton = Button(self,text='Add', command=lambda: DB.Add())
# 			AddButton.grid(row=5, column=1)
#
#
class ViewPage(Frame):


	def __init__(self,parent,controller):
			Frame .__init__(self,parent)


			MonthLabel = Label(self,text='Month')
			MonthLabel.pack(side=TOP, anchor=W)
			month=StringVar()
			EntryMonth = Entry(self,textvariable = month)
			EntryMonth.pack(side=TOP, anchor=W)
			month.set('2019-01')

			global tree


			columnNames =('ID','Date','Type','Category','Amount','Payment')
			scroll = ttk.Scrollbar(self,orient='vertical')
			tree = ttk.Treeview(self,columns = columnNames, yscrollcommand = scroll.set)
			scroll.config(command = tree.yview)
			for column in columnNames:
				tree.heading(column,text = column)
				tree.column(column)#,width=100)
			#delets first empty column
			tree['show']='headings'

			scroll.pack(side=RIGHT, fill=Y)
			tree.pack(side=LEFT,fill=BOTH)
			print(month.get())
			RefreshButton = Button(self,text='Refresh', command=lambda: DB.Refresh(str(month.get())))#Database.Refresh(str(month.get())))
			RefreshButton.pack()


			global db_rows
			# print(MonthEntry2.get())
			records = tree.get_children()
			#db_rows = DB.c.execute("SELECT ID,Date,Type,Category, Amount, Payment from dane where SUBSTR(Date,1,7) = ?",(str(MonthEntry2.get())[0:7],))
			db_rows = DB.c.execute("SELECT ID,Date,Type,Category, Amount, Payment from dane where SUBSTR(Date,1,7) = ?",(str(month.get())[0:7],))
			for row in db_rows:

				tree.insert('',0, values=(row[0], row[1],row[2],row[3],row[4],row[5]))


class Database:

	db = sql.connect('C:\\Projects\\Python\\GitHub\\budget\\Budget_GUI\\Budget.db')
	c = db.cursor()


	def Refresh(self, month):

		self.month = month
		#print(MonthEntry2)
		for a in PrzychodyVariables:
			PrzychodyVariables[a].set(self.GetAmount(a,str(self.month)[0:7]))
			#print(a)

		# dletes all current rows from tree
		for line in tree.get_children():
			tree.delete(line)
		db_rows = DB.c.execute("SELECT ID,Date,Type,Category, Amount, Payment from dane where SUBSTR(Date,1,7) = ?",(str(self.month)[0:7],))

		for row in db_rows:
			tree.insert('',0,text=row[0], values=(row[1], row[2],row[3],row[4],row[5]))


		#print('refreshed')
	def CreateTable(self):

		self.c.execute('''CREATE TABLE IF NOT EXISTS dane(ID INTEGER PRIMARY KEY, Date DATE,
		 Type TEXT, Category TEXT, Amount REAL, Payment TEXT)''')

	def Commit(self):

		self.db.commit()

	def Add(self):
		# print(EntryDateVariable.get(),EntryAmount,EntryAmount.get())

		self.c.execute('INSERT INTO dane(Date, Type, Category, Amount, Payment) VALUES(?,?,?,?,?)',
			(str(EntryDateVariable.get()), str(Type.get()), str(Category.get()), str(EntryAmount.get()), str(Payment.get())))
		self.db.commit()
		self.Refresh(str(MonthEntry2.get()))

	def GetAmount(self,CategoryName,YearMonth):
		self.YearMonth=YearMonth
		#print(self.YearMonth, CategoryName)
		self.c.execute('SELECT SUM(Amount) FROM dane where SUBSTR(Date,1,7) = ? AND Category =?',[str(YearMonth), str(CategoryName)])
		ValueTemp = self.c.fetchall()
		Value = [Value1[0] for Value1 in ValueTemp]
		length = len(str(Value)) - 1

		# print(str(Value)=='[None]')
		if str(Value) == '[None]':
			return 0.00
		else:
			return round(float(str(Value)[1:length]), 2)

	def GetValue(self,CategoryName):
		self.c.execute('SELECT SUM(Amount) FROM dane where Payment =?', [str(CategoryName)])
		ValueTemp = self.c.fetchall()
		Value = [Value1[0] for Value1 in ValueTemp]
		length = len(str(Value)) - 1

		# print(str(Value)=='[None]')
		if str(Value) == '[None]':
			return 0.00
		else:
			return round(float(str(Value)[1:length]), 2)


app = Window()
app.geometry('800x600')
app.title('Budget')
app.mainloop()
