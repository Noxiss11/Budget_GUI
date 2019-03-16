#-*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3 as sql
import datetime
import locale
import matplotlib

from matplotlib import style
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation

style.use('ggplot')


locale.setlocale(locale.LC_ALL,'')


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

	def NumFormat(self,number):
		self.number = float(number)
		return('{:,.2f}'.format(self.number))

#main class for for frame taht will be always open and in which we will see all the pages
class Window(Tk):

	def __init__(self):
		global DB
		DB=Database()
		DB.CreateTable()
		#creates container for all pages
		Tk.__init__(self)
		self.container = Frame(self)
		self.container.pack(side="top", fill="both", expand = "True")

		self.container.grid_rowconfigure(0,weight=1)
		self.container.grid_columnconfigure(0,weight=1)

		menubar = MenuBar(self.container)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label='save settings',)
		self.config(menu=menubar)



		#creates dictionary for list of all pages
		self.frames = {}
		#creates the pages from the dictionary
		for F in (StartPage, MainPage, ViewPage, IncomeGraph,ExpenditureGraph): #AddPage
			frame = F(self.container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0,sticky='nsew')

		self.show_frame(StartPage)

	def refresh_frame(self,page):
		frame = page(self.container, self)
		self.frames[page] = frame
		frame.grid(row=0, column=0,sticky='nsew')
	def refresh_frame2(self,page):
		frame = page(self.container, self)
		self.frames[page] = frame
		frame.grid(row=0, column=0,sticky='nsew')

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
		GraphsMenu.add_command(label='Incomes', command = lambda: app.show_frame(IncomeGraph))
		GraphsMenu.add_command(label='Expenditures', command = lambda: app.show_frame(ExpenditureGraph))
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

			global RozchodyVariables, PrzychodyVariables, namesVariables, MonthEntry2, RetirementValue,EmergencyValue,TargetValue, EntertainmentValue, CashValue, eKontoValue, eMaxValue, Przychody, Rozchody


			names = ['eKonto','Cash','eMax','Retirement','Target','Emergency','Fun']
			Przychody = ['Wynagrodzenie', 'Przychody z kapitalu', 'Inne przychody']
			Rozchody = ['Zywnosc', 'Transport', 'Odziez', 'Telefon', 'Higiena', 'Zdrowie', 'Edukacja', 'Rekreacja', 'Uzywki',
			'Dary', 'Inne', 'Oplaty', 'Srodki trwale', 'Mieszkanie', 'Oplaty mieszkanie', 'Wspolne']

			

			RozchodyVariables = {}
			PrzychodyVariables = {}
			namesVariables = {}

			YearMonth = DateFunctions.CurrentYearMonth
			MonthLabel = Label(self,text='Month')
			MonthLabel.grid(row=0,column=0, sticky = 'w')

			MonthEntryVariable = StringVar()
			MonthEntryVariable .set(DateFunctions.CurrentYearMonth)


			MonthEntry = Entry(self,textvariable = MonthEntryVariable)
			MonthEntry.grid(row=0,column=1, sticky = 'w')
			MonthEntry2 = MonthEntry

			LabelRetirement = Label(self,text='Retirement')
			LabelRetirement.grid(row=3,column=0, sticky = 'w')
			RetirementValue = StringVar()
			DB.RefreshRetirement()
			LabelRetirementValue = Label(self, textvariable =RetirementValue)
			LabelRetirementValue.grid(row=3,column=1, sticky = 'w')
			print(DateFunctions.NumFormat(self,float(RetirementValue.get())))
			# emergency labels and values
			LabelEmergency = Label(self,text='Emergency')
			LabelEmergency.grid(row=4,column=0, sticky = 'w')
			EmergencyValue = StringVar()
			DB.RefreshEmergency()
			LabelEmergencyValue = Label(self,textvariable= EmergencyValue)
			LabelEmergencyValue.grid(row=4,column=1, sticky = 'w')

			# target labels and values
			LabelTarget = Label(self,text='Target')
			LabelTarget.grid(row=5,column=0, sticky = 'w')
			TargetValue = StringVar()
			DB.RefreshTarget()
			LabelTargetValue = Label(self,textvariable= TargetValue)
			LabelTargetValue.grid(row=5,column=1, sticky = 'w')
			
			# entertainment labels and values
			LabelEntertainment = Label(self,text='Entertainment')
			LabelEntertainment.grid(row=6,column=0, sticky = 'w')
			EntertainmentValue = StringVar()
			DB.RefreshEntertainment()
			LabelEntertainmentValue = Label(self,textvariable= EntertainmentValue)
			LabelEntertainmentValue.grid(row=6,column=1, sticky = 'w')
			
			#eMax labels and values 
			LabeleMax = Label(self, text='eMax', anchor='w')
			LabeleMax.grid(row=7,column=0, sticky = 'w')
			eMaxValue = StringVar()
			DB.RefresheMax()

			LabeleMaxValue = Label(self, textvariable = eMaxValue)
			LabeleMaxValue.grid(row=7,column=1, sticky = 'w')

			#cash labels and values
			LabelCash= Label(self,text='Cash')
			LabelCash.grid(row=9,column=0, sticky = 'w')
			CashValue = StringVar()
			DB.RefreshCash()
			LabelCashValue = Label(self,textvariable= CashValue)
			LabelCashValue.grid(row=9,column=1, sticky = 'w')

			#eKonto labels and values
			LabeleKonto= Label(self,text='eKonto')
			LabeleKonto.grid(row=10,column=0, sticky = 'w')
			eKontoValue = StringVar()
			DB.RefresheKonto()
			LabeleKonotValue = Label(self,textvariable= eKontoValue)
			LabeleKonotValue.grid(row=10,column=1, sticky = 'w')
			


			i=12
   
			#############
			##PRZYCHODY##
			#############
			i=i+2
			PrzychodySum=0
			for name in Przychody:
				LabelName = Label(self,text=name)
				LabelName.grid(row=i, column=0, sticky = 'w')

				#PrzychodyVariables[name] = DB.GetAmount(name,MonthEntryVariable.get())
				PrzychodyVariables[name]=StringVar()
				PrzychodyVariables[name].set('{:,.2f}'.format(DB.GetAmount(name,MonthEntryVariable.get())))
				PrzychodySum += DB.GetAmount(name,MonthEntryVariable.get())
				LabelValue = Label(self,textvariable = PrzychodyVariables[name])
				LabelValue.grid(row=i,column=1, sticky = 'w')

				i=i+1


			#Przychody labels and values 
			LabelPrzychody = Label(self, text='Total income', anchor='w')
			LabelPrzychody.grid(row=i,column=0, sticky = 'w')
			PrzychodyValue = StringVar()
			PrzychodyValue.set(PrzychodySum)
			PrzychodyValue = Label(self,textvariable = PrzychodyValue)
			PrzychodyValue.grid(row=i,column=1, sticky = 'w')

			############
			##ROZCHODY##
			############
			i=i-len(Przychody)
			for name in Rozchody:
				LabelName = Label(self,text=name)
				LabelName.grid(row=i, column=3, sticky = 'w')

				RozchodyVariables[name]=StringVar()
				RozchodyVariables[name].set('{:,.2f}'.format(DB.GetAmount(name,MonthEntryVariable.get())))

				LabelValue = Label(self,textvariable = RozchodyVariables[name])
				LabelValue.grid(row=i,column=4, sticky = 'w')

				i=i+1


			RefreshButton = Button(self,text = 'Refresh', command = lambda: DB.Refresh(str(MonthEntry2.get())))
			RefreshButton.grid(row = 0, column =2, sticky = 'w')
			global ValueTest
			ValueTest=StringVar()
			ValueTest.set(DB.GetAmount('Wynagrodzenie',MonthEntryVariable.get()))

			LabelValueTest= Label(self,textvariable=ValueTest)
			LabelValueTest.grid(row=7,column=7, sticky = 'w')

			extrabutton = Button(self,text='add',command = lambda: self.adding())
			extrabutton.grid(row =3, column=5, sticky = 'w')

	def adding(self):

		popup = tk.Tk()

		Przychody = ['Wynagrodzenie', 'Przychody z kapitalu', 'Inne przychody']

		Rozchody = ['Zywnosc', 'Transport', 'Odziez', 'Telefon', 'Higiena', 'Zdrowie', 'Edukacja', 'Rekreacja', 'Uzywki',
		'Dary', 'Inne', 'Oplaty', 'Srodki trwale', 'Mieszkanie', 'Oplaty mieszkanie', 'Wspolne']

		Transfer = ['Cash-->eKonto', 'eKonto-->eMax plus-Emerytura', 'eKonto-->eMax plus-Cel dlugo-dystansowy',
		'eKonto-->eMax-Emergency',
		'eKonto-->eMax-Fundusz rozrywkowy', 'eKonto-->Cash', 'eKonto-->Obligacje-Emerytura',
		'eKonto-->Obligacje-Cel dlugo-dystansowy',
		'eMax plus-Emerytura-->eKonto', 'eMax plus-Cel dlugo-dystansowy-->eKonto', 'eMax-Emergency-->eKonto',
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
			LabelName.grid(row=i, column=0, sticky='w')
			i=i+1

		global EntryDateVariable,EntryAmount, Payment

		#fills the date entry with current date, varaiable is created based on popup object
		EntryDateVariable = StringVar(popup)
		EntryDateVariable .set(DateFunctions.CurrentDate)

		EntryDate = Entry(popup,textvariable=EntryDateVariable)
		EntryDate.grid(row=0,column=1, sticky='w')

		Type = StringVar(popup)
		Type.set('Rozchody')

		LabelType = Label(popup,text='Type')
		LabelType.grid(row=1, column=0, sticky='w')

		OptionType = OptionMenu(popup, Type, *Types)
		OptionType.grid(row=1, column=1, sticky = 'w')

		# trace varaible and change drop down
		Type.trace('w', set_options)

		Category = StringVar(popup)
		Category.set('Zywnosc')

		LabelCategory = Label(popup,text='Category')
		LabelCategory.grid(row=2, column=0, sticky='w')

		OptionCategory = OptionMenu(popup, Category, 'Zywnosc')
		OptionCategory.grid(row=2, column=1, sticky='w')

		EntryAmount = Entry(popup,width=9)
		EntryAmount.grid(row=3, column=1,sticky='w')


		Payment = StringVar(popup)
		Payment.set('eKonto')

		OptionPayment = OptionMenu(popup, Payment, *Payments)
		OptionPayment.grid(row=4, column=1, sticky = 'w')

		AddButton = Button(popup,text='Add', command=lambda: DB.Add())
		AddButton.grid(row=5, column=1, sticky='w')


		def DestroyPopup():
			popup.destroy()

		popup.geometry('400x400')
		popup.title('Add')
		popup.mainloop()

class ViewPage(Frame):


	def __init__(self,parent,controller):
			Frame .__init__(self,parent)


			MonthLabel = Label(self,text='Month')
			MonthLabel.pack(side=TOP, anchor=W)
			month=StringVar()
		
			EntryMonth = Entry(self,textvariable = month)
			EntryMonth.config(width=10)
			EntryMonth.pack(side=TOP, anchor=W)
			month.set(DateFunctions.CurrentYearMonth)
			RefreshButton = Button(self,text='Refresh', command=lambda: DB.Refresh(str(month.get())))#Database.Refresh(str(month.get())))
			RefreshButton.pack(anchor = 'w')


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
			

			global db_rows
			# print(MonthEntry2.get())
			records = tree.get_children()
			#db_rows = DB.c.execute("SELECT ID,Date,Type,Category, Amount, Payment from dane where SUBSTR(Date,1,7) = ?",(str(MonthEntry2.get())[0:7],))
			db_rows = DB.c.execute("SELECT ID,Date,Type,Category, Amount, Payment from dane where SUBSTR(Date,1,7) = ?",(str(month.get())[0:7],))
			for row in db_rows:

				tree.insert('',0, values=(row[0], row[1],row[2],row[3],row[4],row[5]))

class IncomeGraph(Frame):
	def __init__(self,parent,controller):
			
			Frame .__init__(self,parent) 
			self.f = Figure(figsize = (5,5), dpi=100) 
			self.aplot = self.f.add_subplot(111)
			self.incomes = []
			self.monthIncome = 0
			self.months = DB.GetMonths()
			for month in self.months:
				for income in Przychody:
					self.monthIncome += float(DB.GetAmount(income,month))

				self.incomes.append(self.monthIncome)
				self.monthIncome = 0

			self.aplot.plot(self.months,self.incomes)
			print(DB.GetMonths())

			self.canvas = FigureCanvasTkAgg(self.f,self)
			self.canvas.draw()
			self.canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand = True)

	def refresh(self):
		self.incomes = []
		self.monthIncome = 0
		self.months = DB.GetMonths()
		for month in self.months:
			for income in Przychody:
				self.monthIncome += float(DB.GetAmount(income,month))
			self.incomes.append(self.monthIncome)
			self.monthIncome = 0
			#print(self.months,self.incomes)
		self.aplot.clear()
		self.aplot.plot(self.months,self.incomes)
		self.canvas.draw()


class ExpenditureGraph(Frame):
	
	def __init__(self,parent,controller):

			Frame.__init__(self,parent) 
			self.f = Figure(figsize = (5,5), dpi=100) 
			self.bplot = self.f.add_subplot(111)
			self.expenditures = []
			self.monthExpenditures = 0
			self.months = DB.GetMonths()

			for month in self.months:
				for expenditure in Rozchody:
					self.monthExpenditures += float(DB.GetAmount(expenditure, month))
				self.expenditures.append(self.monthExpenditures)
				self.monthExpenditures = 0

			self.bplot.plot(self.months,self.expenditures)
			self.canvasex = FigureCanvasTkAgg(self.f,self)
			self.canvasex.draw()
			self.canvasex.get_tk_widget().pack(side=TOP,fill=BOTH, expand = True)

	def refresh(self):
		self.expenditures = []
		self.monthExpenditures = 0
		self.months = DB.GetMonths()
		for month in self.months:
			for expenditure in Rozchody:
				self.monthExpenditures += float(DB.GetAmount(expenditure,month))
			self.expenditures.append(self.monthExpenditures)
			self.monthExpenditures = 0
			#print(self.months,self.expenditures)
		self.bplot.clear()
		self.bplot.plot(self.months,self.expenditures)
		self.canvasex.draw()


class Database:

	db = sql.connect('Budget.db')
	c = db.cursor()

	def RefreshRetirement(self):
		Value = (float(self.GetValue('eKonto-->eMax plus-Emerytura'))
                       + float(self.GetValue('eMax plus-Emerytura'))
                       - float(self.GetValue('eMax plus-Emerytura-->eKonto')))

		print(float(self.GetValue('eKonto-->eMax plus-Emerytura')),
                        float(self.GetValue('eMax plus-Emerytura')),
                        float(self.GetValue('eMax plus-Emerytura-->eKonto')))
		# Value = DateFunctions.NumFormat(self,Value)
		RetirementValue.set(Value)

	def RefreshTarget(self):
		Value = (self.GetValue('eKonto-->eMax plus-Cel dlugo-dystansowy')
					+ self.GetValue('eMax plus-Cel dlugo-dystansowy')
					- self.GetValue('eMax plus-Cel dlugo-dystansowy-->eKonto'))

		TargetValue.set(Value)

	def RefreshEmergency(self):
		Value = (self.GetValue('eKonto-->eMax-Emergency')
		+ self.GetValue('eMax-Emergency')
		- self.GetValue('eMax-Emergency-->eKonto'))
		EmergencyValue.set(Value)

	def RefreshEntertainment(self):
		Value = (self.GetValue('eKonto-->eMax-Fundusz rozrywkowy')
		+ self.GetValue('eMax-Fundusz rozrywkowy')
		- self.GetValue('Max-Fundusz rozrywkowy-->eKonto'))
		EntertainmentValue.set(Value)

	def RefresheKonto(self):
		Value =  (self.GetValue('eKonto')
                    + self.GetValue('Cash-->eKonto')
                    + self.GetValue('eMax plus-Emerytura-->eKonto')
                    + self.GetValue('eMax-Emergency-->eKonto')
                    + self.GetValue('eMax plus-Cel dlugo-dystansowy-->eKonto')
                    + self.GetValue('Max-Fundusz rozrywkowy-->eKonto')
                    - self.GetValue('eKonto-->eMax plus-Emerytura')
                    - self.GetValue('eKonto-->eMax-Emergency')
                    - self.GetValue('eKonto-->eMax plus-Cel dlugo-dystansowy')
                    - self.GetValue('eKonto-->eMax-Fundusz rozrywkowy')
                    - self.GetValue('eKonto-->Cash'))
		Value = DateFunctions.NumFormat(self,Value)
		eKontoValue.set(Value)

	def RefreshCash(self):
		Value =  (self.GetValue('Cash')
                  + self.GetValue('eKonto-->Cash')
                  - self.GetValue('Cash-->eKonto'))
		
		Value = DateFunctions.NumFormat(self,Value)
		CashValue.set(Value)

	def RefresheMax(self):
		
		Value = (float(RetirementValue.get()) + float(TargetValue.get())+float(EmergencyValue.get())+float(EntertainmentValue.get())) 
		Value = DateFunctions.NumFormat(self,Value)
		eMaxValue.set(Value)
	
	def Refresh(self, month):

		###############
		#incomes##
		###############
		# incomes = []
		# monthIncome = 0
		# months = DB.GetMonths()
		# for month in months:
		# 	for income in Przychody:
		# 		monthIncome += float(DB.GetAmount(income,month))
		# 	incomes.append(monthIncome)
		# 	monthIncome = 0
		# aplot.clear()
		# aplot.plot(months,incomes)
		
		# canvas.draw()
		
		# refreshes the income graph
		app.frames[IncomeGraph].refresh()
		
		# refreshes the spenidnigs graph
		app.frames[ExpenditureGraph].refresh()
		##############
		DB.RefreshRetirement()
		DB.RefreshTarget()
		DB.RefreshEntertainment()
		DB.RefreshEmergency()
		DB.RefresheMax()
		DB.RefreshCash()
		DB.RefresheKonto()
		
				#refreshes value of przychody 
		self.month = month
		for a in PrzychodyVariables:
			PrzychodyVariables[a].set(self.GetAmount(a,str(self.month)[0:7]))

		
		#refreshes value of rozchody 
		self.month = month
		for a in RozchodyVariables:
			RozchodyVariables[a].set(self.GetAmount(a,str(self.month)[0:7]))	
		#
		#TreeView 
		#
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
			(str(EntryDateVariable.get()), str(Type.get()), str(Category.get()), str(EntryAmount.get()).replace(',','.'), str(Payment.get())))
		self.db.commit()
		self.Refresh(str(MonthEntry2.get()))
		# app.destroy()
		# app.__init__()

	def GetAmount(self,CategoryName,YearMonth):
		'''
			pass CategoryName and YearMonth
		'''
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

	
	def GetValue2(self,CategoryName,YearMonth):
		self.YearMonth = str(YearMonth) + '-01'
		self.c.execute('SELECT SUM(Amount) FROM dane where Payment =? AND Date <date(?) ', [str(CategoryName), str(self.YearMonth)])
		ValueTemp = self.c.fetchall()
		Value = [Value1[0] for Value1 in ValueTemp]
		length = len(str(Value)) - 1

		# print(str(Value)=='[None]')
		if str(Value) == '[None]':
			return 0.00
		else:
			return round(float(str(Value)[1:length]), 2)

	def GetMonths(self):

		self.c.execute('SELECT DISTINCT SUBSTR(Date,1,7) as d from dane ORDER BY d ASC') 
		ValueTemp = self.c.fetchall()
		Value = [Value1[0] for Value1 in ValueTemp]
		return Value

app = Window()
app.geometry('800x600')
app.title('Budget')
app.mainloop()
