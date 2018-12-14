########### to do 
# add rest of accouts and create a select statements for them

import tkinter as tk
import sqlite3 as sql
import datetime

db = sql.connect('Budget.db')
c = db.cursor()


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

Types = ('Przychody', 'Rozchody', 'Transfer')
Payments = (
'eKonto', 'Cash', 'eMax plus-Emerytura', 'eMax plus-Cel dlugo-dystansowy', 'eMax-Emergency', 'eMax-Fundusz rozrywkowy')
Amounts = []

c.execute(
    'CREATE TABLE IF NOT EXISTS dane(ID INTEGER PRIMARY KEY, Date DATE, Type TEXT, Category TEXT, Amount REAL, Payment TEXT)')

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


def set_options(*args):
    global Type, Category, OptionCategory, OptionPayment

    if Type.get() == '(default)':
        return None

    # refresh Category
    Category.set('(select)')
    OptionCategory['menu'].delete(0, 'end')

    # pick new set of options

    if Type.get() == 'Przychody':
        new_options = Przychody
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


def Add():
    c.execute('INSERT INTO dane(Date, Type, Category, Amount, Payment) VALUES(?,?,?,?,?)',
              (str(EntryDate.get()), str(Type.get()), str(Category.get()), str(EntryAmount.get()), str(Payment.get())))
    db.commit()
    RefresheKonto()


def GetAmount(CategoryName):
    c.execute('SELECT SUM(Amount) FROM dane where SUBSTR(date,1,7) = ? AND Category =?',
              [str(EntryMonthYear.get()), str(CategoryName)])
    ValueTemp = c.fetchall()
    Value = [Value1[0] for Value1 in ValueTemp]
    length = len(str(Value)) - 1

    # print(str(Value)=='[None]')
    if str(Value) == '[None]':
        return 0.00
    else:
        return round(float(str(Value)[1:length]), 2)


def GetValue(CategoryName):
    c.execute('SELECT SUM(Amount) FROM dane where Payment =?', [str(CategoryName)])
    ValueTemp = c.fetchall()
    Value = [Value1[0] for Value1 in ValueTemp]
    length = len(str(Value)) - 1

    # print(str(Value)=='[None]')
    if str(Value) == '[None]':
        return 0.00
    else:
        return round(float(str(Value)[1:length]), 2)


def RefresheKonto():
    global eKontoValue, CashValue, ZywnoscValue, TransportValue, OdziezValue, TelefonValue, HigienaValue, ZdrowieValue
    global EdukacjaValue, RekreacjaValue, UzywkiValue, DaryValue, InneValue, OplatyValue, Srodki_trwaleValue, MieszkanieValue
    global Oplaty_mieszkanieValue, WspolneValue, Rozchody, WynikValue
    global eMaxValue, EmeryturaValue, CelValue, EmergencyValue, RozrywkaValue
    global WynagrodzenieValue, PrzychodyKapValue, InnePrzychodyValue, PrzychodyValue

    eKontoValue.set(GetValue('eKonto')
                    + GetValue('Cash-->eKonto')
                    + GetValue('eMax plus- Emerytura-->eKonto')
                    + GetValue('eMax-Emergency-->eKonto')
                    + GetValue('eMax plus-Cel dlugo-dystansowy-->eKonto')
                    + GetValue('Max-Fundusz rozrywkowy-->eKonto')
                    - GetValue('eKonto-->eMax plus- Emerytura')
                    - GetValue('eKonto-->eMax-Emergency')
                    - GetValue('eKonto-->eMax plus-Cel dlugo-dystansowy')
                    - GetValue('eKonto-->eMax-Fundusz rozrywkowy')
                    - GetValue('eKonto-->Cash'))

    CashValue.set(GetValue('Cash')
                  + GetValue('eKonto-->Cash')
                  - GetValue('Cash-->eKonto'))

    EmeryturaValue.set(GetValue('eKonto-->eMax plus-Emerytura')
                       + GetValue('eMax plus-Emerytura')
                       - GetValue('eMax plus-Emerytura-->eKonto'))

    EmergencyValue.set(GetValue('eKonto-->eMax-Emergency')
                       + GetValue('eMax-Emergency')
                       - GetValue('eMax-Emergency-->eKonto'))

    CelValue.set(GetValue('eKonto-->eMax plus-Cel dlugo-dystansowy')
                 + GetValue('eMax plus-Cel dlugo-dystansowy')
                 - GetValue('eMax plus-Cel dlugo-dystansowy-->eKonto'))

    RozrywkaValue.set(GetValue('eKonto-->eMax-Fundusz rozrywkowy')
                      + GetValue('eMax-Fundusz rozrywkowy')
                      - GetValue('Max-Fundusz rozrywkowy-->eKonto'))

    WynagrodzenieValue.set(GetAmount('Wynagrodzenie'))
    PrzychodyKapValue.set(GetAmount('Przychody z kapitalu'))
    InnePrzychodyValue.set(GetAmount('Inne przychody'))
    PrzychodyValue.set(GetAmount('Wynagrodzenie') + GetAmount('Przychody z kapitalu') + GetAmount('Inne przychody'))

    def GetRozchody():
        Sum = 0
        for i in Rozchody:
            Sum += GetAmount(i)
        return round(Sum, 2)

    RozchodyValue.set(GetRozchody())

    WynikValue.set(
        float(GetAmount('Wynagrodzenie') + GetAmount('Przychody z kapitalu') + GetAmount('Inne przychody')) + float(
            GetRozchody()))
    eMaxSum = float(EmeryturaValue.get()) + float(EmergencyValue.get()) + float(CelValue.get()) + float(
        RozrywkaValue.get())
    eMaxValue.set(eMaxSum)
    ZywnoscValue.set(GetAmount('Zywnosc'))
    TransportValue.set(GetAmount('Transport'))
    OdziezValue.set(GetAmount('Odziez'))
    TelefonValue.set(GetAmount('Telefon'))
    HigienaValue.set(GetAmount('Higiena'))
    ZdrowieValue.set(GetAmount('Zdrowie'))
    EdukacjaValue.set(GetAmount('Edukacja'))
    RekreacjaValue.set(GetAmount('Rekreacja'))
    UzywkiValue.set(GetAmount('Uzywki'))
    DaryValue.set(GetAmount('Dary'))
    InneValue.set(GetAmount('Inne'))
    OplatyValue.set(GetAmount('Oplaty'))
    Srodki_trwaleValue.set(GetAmount('Srodki trwale'))
    MieszkanieValue.set(GetAmount('Mieszkanie'))
    Oplaty_mieszkanieValue.set(GetAmount('Oplaty mieszkanie'))
    WspolneValue.set(GetAmount('Wspolne'))


root = tk.Tk()
root.title('Budget')

# AmountCalc()

LabelDate = tk.Label(text='Date')
LabelDate.grid(row=0, column=0)

SelectedDate = tk.StringVar(root)
SelectedDate.set(CurrentDate)

EntryDate = tk.Entry(textvariable=SelectedDate, width=10)
EntryDate.grid(row=0, column=1)

SelectedMonth = tk.StringVar(root)
SelectedMonth.set(CurrentYearMonth)

EntryMonthYear = tk.Entry(textvariable=SelectedMonth, width=7)
EntryMonthYear.grid(row=0, column=2)

# drop down to determinate secound group down
Type = tk.StringVar(root)
Type.set('Rozchody')

LabelType = tk.Label(text='Type')
LabelType.grid(row=1, column=0)

OptionType = tk.OptionMenu(root, Type, *Types)
OptionType.grid(row=1, column=1)

# trace varaible and change drop down
Type.trace('w', set_options)

# secound drop down
Category = tk.StringVar(root)
Category.set('Zywnosc')

LabelCategory = tk.Label(text='Category')
LabelCategory.grid(row=2, column=0)

OptionCategory = tk.OptionMenu(root, Category, 'Zywnosc')
OptionCategory.grid(row=2, column=1)

LabelAmount = tk.Label(text='Amount')
LabelAmount.grid(row=4, column=0)

EntryAmount = tk.Entry(width=9)
EntryAmount.grid(row=4, column=1)

LabelPayment = tk.Label(text='Payment')
LabelPayment.grid(row=5, column=0)

Payment = tk.StringVar()
Payment.set('eKonto')

OptionPayment = tk.OptionMenu(root, Payment, *Payments)
OptionPayment.grid(row=5, column=1)

AddButton = tk.Button(text='Add', command=Add)
AddButton.grid(row=5, column=2)

LabeleKonto = tk.Label(text='eKonto')
LabeleKonto.grid(row=0, column=4)

eKontoValue = tk.StringVar()
eKontoValue.set('(-)')

LabeleKontoValue = tk.Label(textvariable=eKontoValue)
LabeleKontoValue.grid(row=0, column=5)

CashValue = tk.StringVar()
CashValue.set('(-)')

LabelCash = tk.Label(text='Cash')
LabelCash.grid(row=1, column=4)

LabelCashValue = tk.Label(textvariable=CashValue)
LabelCashValue.grid(row=1, column=5)

eMaxValue = tk.StringVar()
eMaxValue.set('(-)')

LabeleMax = tk.Label(text='eMax')
LabeleMax.grid(row=2, column=4)

LabeleMaxValue = tk.Label(textvariable=eMaxValue)
LabeleMaxValue.grid(row=2, column=5)

EmeryturaValue = tk.StringVar()
EmeryturaValue.set('(-)')

LabelEmerytura = tk.Label(text='Emerytura')
LabelEmerytura.grid(row=3, column=4)

LabelEmeryturaValue = tk.Label(textvariable=EmeryturaValue)
LabelEmeryturaValue.grid(row=3, column=5)

CelValue = tk.StringVar()
CelValue.set('(-)')

LabelCel = tk.Label(text='Cel')
LabelCel.grid(row=4, column=4)

LabelCelValue = tk.Label(textvariable=CelValue)
LabelCelValue.grid(row=4, column=5)

EmergencyValue = tk.StringVar()
EmergencyValue.set('(-)')

LabelEmergency = tk.Label(text='Emergency')
LabelEmergency.grid(row=5, column=4)

LabelEmergencyValue = tk.Label(textvariable=EmergencyValue)
LabelEmergencyValue.grid(row=5, column=5)

RozrywkaValue = tk.StringVar()
RozrywkaValue.set('(-)')

LabelRozrywka = tk.Label(text='Rozrywka')
LabelRozrywka.grid(row=6, column=4)

LabelRozrywkaValue = tk.Label(textvariable=RozrywkaValue)
LabelRozrywkaValue.grid(row=6, column=5)

ButtonRefresh = tk.Button(text='Refresh', command=RefresheKonto)
ButtonRefresh.grid(row=1, column=2)

LabelZywnosc = tk.Label(text='Zywnosc')
LabelZywnosc.grid(row=8, column=0)

ZywnoscValue = tk.StringVar()
ZywnoscValue.set('(-)')

LabelZywnoscValue = tk.Label(textvariable=ZywnoscValue)
LabelZywnoscValue.grid(row=8, column=1)

LabelTelefon = tk.Label(text='Telefon')
LabelTelefon.grid(row=9, column=0)

TelefonValue = tk.StringVar()
TelefonValue.set('(-)')

LabelTelefonValue = tk.Label(textvariable=TelefonValue)
LabelTelefonValue.grid(row=9, column=1)

LabelTransport = tk.Label(text='Transport')
LabelTransport.grid(row=10, column=0)

TransportValue = tk.StringVar()
TransportValue.set('(-)')

LabelTransportValue = tk.Label(textvariable=TransportValue)
LabelTransportValue.grid(row=10, column=1)

LabelOdziez = tk.Label(text='Odziez')
LabelOdziez.grid(row=11, column=0)

OdziezValue = tk.StringVar()
OdziezValue.set('(-)')

LabelOdziezValue = tk.Label(textvariable=OdziezValue)
LabelOdziezValue.grid(row=11, column=1)

LabelHigiena = tk.Label(text='Higiena')
LabelHigiena.grid(row=12, column=0)

HigienaValue = tk.StringVar()
HigienaValue.set('(-)')

LabelHigienaValue = tk.Label(textvariable=HigienaValue)
LabelHigienaValue.grid(row=12, column=1)

LabelDary = tk.Label(text='Dary')
LabelDary.grid(row=13, column=0)

DaryValue = tk.StringVar()
DaryValue.set('(-)')

LabelDaryValue = tk.Label(textvariable=DaryValue)
LabelDaryValue.grid(row=13, column=1)

LabelInne = tk.Label(text='Inne')
LabelInne.grid(row=14, column=0)

InneValue = tk.StringVar()
InneValue.set('(-)')

LabelInneValue = tk.Label(textvariable=InneValue)
LabelInneValue.grid(row=14, column=1)

LabelOplaty = tk.Label(text='Oplaty')
LabelOplaty.grid(row=15, column=0)

OplatyValue = tk.StringVar()
OplatyValue.set('(-)')

LabelOplatyValue = tk.Label(textvariable=OplatyValue)
LabelOplatyValue.grid(row=15, column=1)

LabelSrodki_trwale = tk.Label(text='Srodki_trwale')
LabelSrodki_trwale.grid(row=16, column=0)

Srodki_trwaleValue = tk.StringVar()
Srodki_trwaleValue.set('(-)')

LabelSrodki_trwaleValue = tk.Label(textvariable=Srodki_trwaleValue)
LabelSrodki_trwaleValue.grid(row=16, column=1)

LabelMieszkanie = tk.Label(text='Mieszkanie')
LabelMieszkanie.grid(row=17, column=0)

MieszkanieValue = tk.StringVar()
MieszkanieValue.set('(-)')

LabelMieszkanieValue = tk.Label(textvariable=MieszkanieValue)
LabelMieszkanieValue.grid(row=17, column=1)

LabelOplaty_mieszkanie = tk.Label(text='Oplaty_mieszkanie')
LabelOplaty_mieszkanie.grid(row=18, column=0)

Oplaty_mieszkanieValue = tk.StringVar()
Oplaty_mieszkanieValue.set('(-)')

LabelOplaty_mieszkanieValue = tk.Label(textvariable=Oplaty_mieszkanieValue)
LabelOplaty_mieszkanieValue.grid(row=18, column=1)

LabelWspolne = tk.Label(text='Wspolne')
LabelWspolne.grid(row=19, column=0)

WspolneValue = tk.StringVar()
WspolneValue.set('(-)')

LabelWspolneValue = tk.Label(textvariable=WspolneValue)
LabelWspolneValue.grid(row=19, column=1)

LabelEdukacja = tk.Label(text='Edukacja')
LabelEdukacja.grid(row=20, column=0)

EdukacjaValue = tk.StringVar()
EdukacjaValue.set('(-)')

LabelEdukacjaValue = tk.Label(textvariable=EdukacjaValue)
LabelEdukacjaValue.grid(row=20, column=1)

LabelRekreacja = tk.Label(text='Rekreacja')
LabelRekreacja.grid(row=21, column=0)

RekreacjaValue = tk.StringVar()
RekreacjaValue.set('(-)')

LabelRekreacjaValue = tk.Label(textvariable=RekreacjaValue)
LabelRekreacjaValue.grid(row=21, column=1)

LabelUzywki = tk.Label(text='Uzywki')
LabelUzywki.grid(row=22, column=0)

UzywkiValue = tk.StringVar()
UzywkiValue.set('(-)')

LabelUzywkiValue = tk.Label(textvariable=UzywkiValue)
LabelUzywkiValue.grid(row=22, column=1)

LabelZdrowie = tk.Label(text='Zdrowie')
LabelZdrowie.grid(row=23, column=0)

ZdrowieValue = tk.StringVar()
ZdrowieValue.set('(-)')

LabelZdrowieValue = tk.Label(textvariable=ZdrowieValue)
LabelZdrowieValue.grid(row=23, column=1)

LabelRozchody = tk.Label(text='Rozchody')
LabelRozchody.grid(row=7, column=0)

RozchodyValue = tk.StringVar()
RozchodyValue.set('(-)')

LabelRozchodyValue = tk.Label(textvariable=RozchodyValue)
LabelRozchodyValue.grid(row=7, column=1)

LabelWynagrodzenie = tk.Label(text='Wynagrodzenie')
LabelWynagrodzenie.grid(row=8, column=2)

WynagrodzenieValue = tk.StringVar()
WynagrodzenieValue.set('(-)')

LabelWynagrodzenieValue = tk.Label(textvariable=WynagrodzenieValue)
LabelWynagrodzenieValue.grid(row=8, column=3)

LabelPrzychodyKap = tk.Label(text='Przychody z kapitalu')
LabelPrzychodyKap.grid(row=9, column=2)

PrzychodyKapValue = tk.StringVar()
PrzychodyKapValue.set('(-)')

LabelPrzychodyKapValue = tk.Label(textvariable=PrzychodyKapValue)
LabelPrzychodyKapValue.grid(row=9, column=3)

LabelInnePrzychody = tk.Label(text='Inne przychody')
LabelInnePrzychody.grid(row=10, column=2)

InnePrzychodyValue = tk.StringVar()
InnePrzychodyValue.set('(-)')

LabelInnePrzychodyValue = tk.Label(textvariable=InnePrzychodyValue)
LabelInnePrzychodyValue.grid(row=10, column=3)

LabelPrzychody = tk.Label(text='Przychody')
LabelPrzychody.grid(row=7, column=2)

PrzychodyValue = tk.StringVar()
PrzychodyValue.set('(-)')

LabelPrzychodyValue = tk.Label(textvariable=PrzychodyValue)
LabelPrzychodyValue.grid(row=7, column=3)

LabelWynik = tk.Label(text='WF')
LabelWynik.grid(row=7, column=4)

WynikValue = tk.StringVar()
WynikValue.set('(-)')

LabelWynikValue = tk.Label(textvariable=WynikValue)
LabelWynikValue.grid(row=7, column=5)

set_options()
RefresheKonto()

tk.mainloop()
