from tkinter import *
import sqlite3 as sql

db = sql.connect('test.db')
c = db.cursor()
Type =('Przychody', 'Rozchody', 'Transfer')
CategoryPrzychody = ('Wynagrodzenie','Przychody z kapitalu')
CategoryRozchody= ('Zywnosc','Transport')
Payment = ('eKonto')

global option, CategoryOption, TypeOption

class SQL():


    def selectSUM():
        c.execute('SELECT ROUND(SUM(Kwota),2) FROM test WHERE Przeplyw = "eKonto"')
        sumSQL = c.fetchall()
        sumSQL = [sumSQL1[0] for sumSQL1 in sumSQL]
        return sumSQL

    def SQLeKonto():
        c.execute('SELECT SUM(Kwota) FROM test WHERE strftime("%m",Data)= ?',(str(Frame.DateSQLEntry.get()),))
        VariableeKonto = c.fetchall()
        VariableeKonto = [VariableeKontoOutput[0] for VariableeKontoOutput in VariableeKonto]
        return VariableeKonto

    def AddNewRecordToDB(DateEntry,TypeOption,CategoryOption,AmountEntry):
        date = str(DateEntry.get())
        typE = str(TypeOption.get())
        category = str(CategoryOption.get())
        amount = str(AmountEntry.get())
        payment = str(AmountEntry.get())
        c.execute('INSERT INTO test(Data,Rodzaj,Kategoria,Kwota,Przeplyw) VALUES(?,?,?,?,?)',(date,typE,category,amount,payment))
        db.commit()





class Window(Frame):

    def __init__(self, master=None):
        ##Defaining stuff to check from tkinter package
        Frame.__init__(self, master)
        self.master = master

        self.init_window()
    ##Initialise the window


    def init_window(self):

        ##Set the title of the window
        self.master.title('Budget')

        self.pack(fill=BOTH, expand=1)

        DateLabel = Label(self, text='Date',borderwidth=2,relief='solid')
        DateLabel.grid(row=0, column=0)

        DateEntry = Entry(self)
        DateEntry.grid(row=0,column=1)

        TypeLabel = Label(self, text='Type')
        TypeLabel.grid(row=1, column=0)

        TypeSelected = StringVar()
        TypeSelected.set(Type[0])

        TypeOption = OptionMenu(self,TypeSelected,*Type)
        TypeOption.grid(row=1, column=1)

        CategoryLabel = Label(self,text='Category')
        CategoryLabel.grid(row=2, column=0)

        CategorySelected = StringVar()


        CategoryOption = OptionMenu(self,CategorySelected,'(selected)')
        CategoryOption.grid(row=2,column=1)


        AmountLabel = Label(self, text='Amount')
        AmountLabel.grid(row=3,column=0)

        AmountEntry = Entry(self)
        AmountEntry.grid(row=3, column=1)

        PaymentLabel = Label(self,text='Payment')
        PaymentLabel.grid(row=4,column=0)

        DateSQLLabel = Label(self,text='Month')
        DateSQLLabel.grid(row=6, column=0)

        eKontoLabel = Label(self,text='eKonto')
        eKontoLabel.grid(row=6,column=1)

        eKontoAmount = StringVar()
        eKontoAmount = str(SQL.selectSUM())

        DateSQLEntry = Entry(self, width=10)
        DateSQLEntry.grid(row=7,column=0)

        eKontoValue = Label(self,text=eKontoAmount)
        eKontoValue.grid(row=7,column=1)

        # eKontoAmount2 = StringVar()
        # eKontoAmount2 = str(SQL.SQLeKonto())

        testing ='asd'

        # eKontoValue2 = Label(self,text=eKontoAmount2)
        # eKontoValue2.grid(row=7,column=2)


        # RefreshButton = Button(self,text='Refresh',command=eKontoRefresh)
        # RefreshButton.grid(row=8,column=0)

def set_Categroy(self):

    # check if something has been selected
    if option.set() == '(select)':
        return None

    # refresh option menu
    option.set('(select)')
    CategoryOption['menu'].delete(0,'end')

    # pick new set of option
    if option.get() == 'Przychody':
        new_options = CategoryPrzychody
    else:
        new_options = CategoryRozchody

    # add new options to
    for item in new_options:
        CategoryOption['menu'].add_command(label=item, command=tkinter._setit(option,item))


root = Tk()
root.geometry('400x300')
app = Window(root)
Window(Frame).set_Category()
print(app.init_window())
root.mainloop()

db.close()