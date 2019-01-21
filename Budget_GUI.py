from tkinter import *
import sqlite3 as sql
import datetime

## Add 0 to days and months that have only one diget
def DateFormat(number):
	if int(number) < 10:
		return "0" + str(number)
	return number


CurrentYearMonth = str(datetime.datetime.date(datetime.datetime.now()).year) + '-' + str(
	datetime.datetime.date(datetime.datetime.now()).month)
CurrentDate = str(datetime.datetime.date(datetime.datetime.now()).year) + '-' + DateFormat(str(
	datetime.datetime.date(datetime.datetime.now()).month)) + '-' + DateFormat(str(
	datetime.datetime.date(datetime.datetime.now()).day))

db = sql.connect('test.db')
c = db.cursor()

c.execute(
	'CREATE TABLE IF NOT EXISTS dane(ID INTEGER PRIMARY KEY, Date DATE, Type TEXT, Category TEXT, Amount REAL, Payment TEXT)')

Type =('Przychody', 'Rozchody', 'Transfer')
CategoryPrzychody = ('Wynagrodzenie','Przychody z kapitalu')
CategoryRozchody= ('Zywnosc','Transport')
Payment = ('eKonto')

global option, CategoryOption, TypeOption

class SQL():


	def selectSUM():
		c.execute('SELECT ROUND(SUM(Kwota),2) FROM dane WHERE Przeplyw = "eKonto"')
		sumSQL = c.fetchall()
		sumSQL = [sumSQL1[0] for sumSQL1 in sumSQL]
		return sumSQL

	def SQLeKonto():
		c.execute('SELECT SUM(Kwota) FROM dane WHERE strftime("%m",Data)= ?',(str(Frame.DateSQLEntry.get()),))
		VariableeKonto = c.fetchall()
		VariableeKonto = [VariableeKontoOutput[0] for VariableeKontoOutput in VariableeKonto]
		return VariableeKonto

	def AddNewRecordToDB(DateEntry,TypeOption,CategoryOption,AmountEntry):
		date = str(DateEntry.get())
		typE = str(TypeOption.get())
		category = str(CategoryOption.get())
		amount = str(AmountEntry.get())
		payment = str(AmountEntry.get())
		c.execute('INSERT INTO dane(Data,Rodzaj,Kategoria,Kwota,Przeplyw) VALUES(?,?,?,?,?)',(date,typE,category,amount,payment))
		db.commit()





class Window(Frame):

	##Initialise the window
	def __init__(self, master=None):
		Frame.__init__(self,master)
		self.init_window()
		#self.init_variables()

	def init_window(Frame):

		row_space = 10
		column_space = 20

		##Set the title of the window
		Frame.master.title('Budget')

		Frame.LabelDate = Label(text='Date')
		Frame.LabelDate.place(x = 0,y = 0)
		

  #   def init_variables(self):
		
  #   	SelectedDate = StringVar()
		# SelectedDate.set(CurrentDate)


	 

		
	


root = Tk()
root.geometry('400x300')
app = Window(root)

print(app.init_window())
root.mainloop()

db.close()