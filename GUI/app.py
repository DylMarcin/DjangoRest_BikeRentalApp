import tkinter as tk
import tkinter.ttk as ttk
import json
from tkinter import *
import os
from PIL import ImageTk, Image
import requests
import ast
from tkinter import messagebox


#Main Screen
master = Tk()
master.title('BicycleRental')

#Functions
def rental_new(variable, temp_bike_id_number):

    if variable.get() == "------" or temp_bike_id_number.get() == "":
        messagebox.showinfo("Alert","Błędnie wypełniono formularz!")
        return
    
    for item in jsonBikesid:
        url = 'http://127.0.0.1:8000/bikes/'+str(item)+'/'
        requests.patch(url, data ={'available': False})


    url = 'http://127.0.0.1:8000/rentals/'
    custom_json = {"client": variable.get(),"bike_id_number": jsonBikes,"returned": False}

    requests.post(url, json = custom_json, headers = {'Content-Type': 'application/json'})

    messagebox.showinfo("Zatwierdzenie","Pomyślnie dodano wypożyczenie")

    CreateRental_Screen.destroy()

def rental_create():

    #AddClientScreen
    global CreateRental_Screen
    CreateRental_Screen = Toplevel(master)
    CreateRental_Screen.title('Add Client')

    #Labels
    Label(CreateRental_Screen, text="Wprowadź dane formularza, aby edytować", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
    Label(CreateRental_Screen, text="Wybierz klienta", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(CreateRental_Screen, text="Wybierz rowery", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(CreateRental_Screen, text=" ", font=('Calibri',12)).grid(row=2,sticky=W)

    notif = Label(CreateRental_Screen, font=('Calibri', 12))
    notif.grid(row=8, sticky=N, pady = 10)

    #Entries
    get_clients = requests.get('http://127.0.0.1:8000/clients/')
    parsed_clients = json.loads(get_clients.text)

    temp_bike_id_number = StringVar()
    variable = StringVar(master)
    variable.set("------")

    lists = []
    jsonBikesid = temp_bike_id_number

    for item in parsed_clients:
        lists.append(item['name'])

    OptionMenu(CreateRental_Screen, variable, *lists).grid(row=1, sticky= N)

    Button(CreateRental_Screen, text="Wybierz", font=('Calibri', 12),width=8, command = lambda: active_bikes(temp_bike_id_number)).grid(row=3, column = 0, sticky=E)
    Entry(CreateRental_Screen, textvariable=temp_bike_id_number, state = 'disabled', width=20).grid(row=3, column=0)

    #Buttons
    Button(CreateRental_Screen, text='Dodaj', font=('Calibri', 12),width=8, command = lambda: rental_new(variable, temp_bike_id_number)).grid(row=9, sticky=N, pady=5)

def close_bike(return_bike_screen, bike_returned_screen):
    return_bike_screen.destroy()
    bike_returned_screen.destroy()
    Rental_Screen.destroy()
    AddRental_Screen.destroy()

    rental_view()

def returned_bike(value, return_bike_screen):

    url = 'http://127.0.0.1:8000/rentals/'+value[0]+'/'
    requests.patch(url, data ={'returned': True})

    r = requests.get('http://127.0.0.1:8000/bikes/')
    loaded = json.loads(r.text)
    
    listed = value[2].split()

    list_of_bikes = []

    for i in range(len(listed)):
        selected_bike_list = list(item for item in loaded if item["bike_id_number"] == listed[i])
        list_of_bikes.append(selected_bike_list)

    array_length = len(list_of_bikes)

    for i in range(array_length):
        url = 'http://127.0.0.1:8000/bikes/'+str(list_of_bikes[i][0]['id'])+'/'
        requests.patch(url, data ={'available': True})

    bike_returned_screen = Toplevel(master)
    bike_returned_screen.title('Potwierdzenie')

    Label(bike_returned_screen, text="Przeniesiono zgloszenie do historii", font=('Calibri',14, "bold italic")).grid(row=0,sticky=N,pady=20, padx=10)

    Button(bike_returned_screen , text='Okej', font=('Calibri', 12),width=8, command= lambda: close_bike(return_bike_screen, bike_returned_screen)).grid(row=2, sticky=N, pady=5)


def false_return(return_bike_screen):
    return_bike_screen.destroy()

    

def returned_bike_screen(value):

    url = 'http://127.0.0.1:8000/rentals/'+value[0]+'/'

    return_bike_screen = Toplevel(master)
    return_bike_screen.title('Potwierdzenie')         

    #Labels   
    Label(return_bike_screen, text="Zatwierdzenie spowoduje przeniesienie zgłoszenia do historii", font=('Calibri',14, "bold italic")).grid(row=0,sticky=N,pady=20, padx=10)
    Label(return_bike_screen, text="Czy chcesz kontynuować?", font=('Calibri',14, "bold italic")).grid(row=1,sticky=N,pady=20, padx=10)

    Button(return_bike_screen , text='Tak', font=('Calibri', 12),width=8, command = lambda: returned_bike(value, return_bike_screen)).grid(row=2, sticky=N, pady=5)
    Button(return_bike_screen , text='Wyjdź', font=('Calibri', 12),width=8, command = lambda: false_return(return_bike_screen)).grid(row=3,sticky=N, pady=5)
    
 
def rental_view():

    def rental_update(variable, temp_bike_id_number, notif, value, AddRental_Screen):

        url = 'http://127.0.0.1:8000/rentals/'+value[0]+'/'

        custom_json = {"client": variable.get(),"bike_id_number": L1,"returned": False}
        

        if variable.get() == "" or temp_bike_id_number.get() == "":
            notif.config(fg="red", text="* Wszystkie pola są wymagane")
            return

        requests.put(url, json = custom_json, headers = {'Content-Type': 'application/json'})
        
        Rental_Screen.destroy()
        AddRental_Screen.destroy()
        
        rental_view()

    def OnDoubleClick(event):

        item = treeview.selection()
        kev = []
        for i in item:
           value = treeview.item(i, "values")

        #Vars
        temp_bike_id_number = StringVar()
        temp_bike_id_number.set(value[2])

        #AddClientScreen
        global AddRental_Screen
        AddRental_Screen = Toplevel(master)
        AddRental_Screen.title('Add Client')

        #Labels
        Label(AddRental_Screen, text="Wprowadź dane formularza, aby edytować", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
        Label(AddRental_Screen, text="Wybierz klienta", font=('Calibri',12)).grid(row=1,sticky=W)
        Label(AddRental_Screen, text="Wybierz rowery", font=('Calibri',12)).grid(row=3,sticky=W)
        
        Label(AddRental_Screen, text=" ", font=('Calibri',12)).grid(row=2,sticky=W)

        notif = Label(AddRental_Screen, font=('Calibri', 12))
        notif.grid(row=8, sticky=N, pady = 10)

        #Entries
        get_clients = requests.get('http://127.0.0.1:8000/clients/')
        parsed_clients = json.loads(get_clients.text)


        variable = StringVar(master)
        variable.set(value[1])

        lists = []

        for item in parsed_clients:
            lists.append(item['name'])

        OptionMenu(AddRental_Screen, variable, *lists).grid(row=1, sticky= N)
        Entry(AddRental_Screen, textvariable=temp_bike_id_number, state = 'disabled', width=20).grid(row=3, column=0)
        Button(AddRental_Screen, text="Wybierz", font=('Calibri', 12),width=8, command = lambda: active_bikes(temp_bike_id_number)).grid(row=3, column = 0, sticky=E)
        notif = Label(AddRental_Screen, font=('Calibri', 12))
        notif.grid(row=8, sticky=N, pady = 10)

        #Buttons
        Button(AddRental_Screen, text='Zapisz', font=('Calibri', 12),width=8, command= lambda: rental_update(variable, temp_bike_id_number, notif, value, AddRental_Screen)).grid(row=9, sticky=N, pady=5)
        Button(AddRental_Screen, text='Zamknij wypożyczenie', font=('Calibri', 12),width=20, command= lambda: returned_bike_screen(value)).grid(row=10, sticky=N, pady=5)
    
    #ActiveRentalsScreen
    global Rental_Screen
    Rental_Screen = Toplevel(master)
    Rental_Screen.title('Active Rentals')

    response = requests.get('http://127.0.0.1:8000/activerentals/')
    parsed = json.loads(response.text)

    Label(Rental_Screen, text="Aktualna lista wypożyczeń w systemie", font=('Calibri',12)).grid(row=17,sticky=N)
    treeview = ttk.Treeview(Rental_Screen, show="headings", columns=('ID', 'Klient', 'Numer Ramy Roweru/ów', 'Data utworzenia'))
    treeview.heading("#1", text="ID")
    treeview.column("#1", minwidth=0, width=20, stretch=NO)
    treeview.heading("#2", text="Klient")
    treeview.column("#2", minwidth=0, width=100, stretch=NO)
    treeview.heading("#3", text="Numer Ramy Roweru/ow")
    treeview.column("#3", minwidth=0, width=400, stretch=NO)
    treeview.heading("#4", text="Data utworzenia")
    treeview.column("#4", minwidth=0, width=100, stretch=NO)
    treeview.grid()

    for row in parsed:
        treeview.insert("", "end", values=(row["id"], row["client"], row["bike_id_number"], row["created"]))
        treeview.bind("<Double-1>", OnDoubleClick)

def active_bikes(temp_bike_id_number):
    
    global jsonBikes
    global jsonBikesid

    response = requests.get('http://127.0.0.1:8000/availablebikes/')
    parsed = json.loads(response.text)

    Active_bike_Screen = Toplevel(master)
    Active_bike_Screen.title('Wybierz rowery')

    listbox = Listbox(Active_bike_Screen, width=40, height=10, selectmode=MULTIPLE)
    listbox2 = Listbox(Active_bike_Screen, width=40, height=10)

    i=0
    selected_bikes = []
    global selected_bikes_id
    

    for items in parsed:
        listbox.insert(i, items['bike_id_number'])
        listbox2.insert(i, items['id'])
        i+=1

    def selected_item(Active_bike_Screen):
        global jsonBikes
        global jsonBikesid
        selected_bikes = []
        selected_bikes_id = []
        for i in listbox.curselection():
            selected_bikes.append(listbox.get(i))
            selected_bikes_id.append(listbox2.get(i))

        temp_bike_id_number.set(selected_bikes)
        jsonBikes = ast.literal_eval(temp_bike_id_number.get())
        jsonBikesid = selected_bikes_id
        Active_bike_Screen.destroy()
        
    Button(Active_bike_Screen, text="Dodaj", font=('Calibri', 12),width=8, command=lambda: selected_item(Active_bike_Screen)).grid(row=1, column = 0, sticky = N)
    listbox.grid(row=0)

# --------------------------------------------------------------------- KLIENT ----------------------------------------------------------------------------------------------------------------------
def create_user(temp_name, temp_tel, temp_id, temp_city, temp_pcode, temp_street, temp_number, notif, AddClient_Screen):
    url = 'http://127.0.0.1:8000/clients/'
    myobj = {
            "name": temp_name.get(),
            "tel": temp_tel.get(),
            "personal_number": temp_id.get(),
            "city": temp_city.get(),
            "zip_code": temp_pcode.get(),
            "street": temp_street.get(),
            "house_number": temp_number.get()
            }
    if temp_name.get() == "" or temp_tel.get() == "" or temp_id.get() == "" or temp_city.get() == "" or temp_pcode.get() == "" or temp_street.get() == "" or temp_number.get() =="" :
            notif.config(fg="red", text="* Wszystkie pola są wymagane")
            return
    requests.post(url, data = myobj)

    Client_confirm = Toplevel(AddClient_Screen)
    Client_confirm.title('Potwierdzenie')         

    #Labels
        
    Label(Client_confirm, text="Klient został dodany do systemu", font=('Calibri',14, "bold italic")).grid(row=0,sticky=N,pady=20, padx=10)
    Button(Client_confirm , text='Zamknij', font=('Calibri', 12),width=8, command=  lambda: client_confirm_create(AddClient_Screen, Client_confirm)).grid(row=8, sticky=N, pady=5)
    
def add_client():
    
    #Vars
    temp_name = StringVar()
    temp_tel = StringVar()
    temp_id = StringVar()
    temp_city = StringVar()
    temp_pcode = StringVar()
    temp_street = StringVar()
    temp_number = StringVar()

    #AddClientScreen
    AddClient_Screen = Toplevel(master)
    AddClient_Screen.title('Add Client')

    #Labels
    Label(AddClient_Screen, text="Wprowadź dane klienta, aby dodać do systemu", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
    Label(AddClient_Screen, text="Imie i Nazwisko", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(AddClient_Screen, text="Telefon", font=('Calibri',12)).grid(row=2,sticky=W)
    Label(AddClient_Screen, text="Numer Dowodu", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(AddClient_Screen, text="Miasto", font=('Calibri',12)).grid(row=4,sticky=W)
    Label(AddClient_Screen, text="Kod Pocztowy", font=('Calibri',12)).grid(row=5,sticky=W)
    Label(AddClient_Screen, text="Ulica", font=('Calibri',12)).grid(row=6,sticky=W)
    Label(AddClient_Screen, text="Numer Domu", font=('Calibri',12)).grid(row=7,sticky=W)
    notif = Label(AddClient_Screen, font=('Calibri', 12))
    notif.grid(row=8, sticky=N, pady = 10)

    #Entries
    Entry(AddClient_Screen, textvariable=temp_name).grid(row=1, column=0)
    Entry(AddClient_Screen, textvariable=temp_tel).grid(row=2, column=0)
    Entry(AddClient_Screen, textvariable=temp_id).grid(row=3, column=0)
    Entry(AddClient_Screen, textvariable=temp_city).grid(row=4, column=0)
    Entry(AddClient_Screen, textvariable=temp_pcode).grid(row=5, column=0)
    Entry(AddClient_Screen, textvariable=temp_street).grid(row=6, column=0)
    Entry(AddClient_Screen, textvariable=temp_number).grid(row=7, column=0)

    #Buttons
    Button(AddClient_Screen, text='Zapisz', font=('Calibri', 12), width=8, command=lambda: create_user(temp_name, temp_tel, temp_id, temp_city, temp_pcode, temp_street, temp_number, notif, AddClient_Screen)).grid(row=9, sticky=N, pady=5)

def client_confirm_create(AddClient_Screen, Client_confirm):
    
    Client_confirm.destroy()
    AddClient_Screen.destroy()

def client_confirm_update(AddClient_Screen, Client_confirm):
    
    Client_confirm.destroy()
    AddClient_Screen.destroy()
    client_view()
    
def client_view():
    
    def update_client(temp_name, temp_tel, temp_id, temp_city, temp_pcode, temp_street, temp_number, value, notif, AddClient_Screen):

        if temp_name.get() == "" or temp_tel.get() == "" or temp_id.get() == "" or temp_city.get() == "" or temp_pcode.get() == "" or temp_street.get() == "" or temp_number.get() =="" :
            notif.config(fg="red", text="* Wszystkie pola są wymagane")
            return

        url = 'http://127.0.0.1:8000/clients/'+value[0]+'/'
        myobj = {"name": temp_name.get(),"tel": temp_tel.get(),"personal_number": temp_id.get(),"city": temp_city.get(),"zip_code": temp_pcode.get(),"street": temp_street.get(),"house_number": temp_number.get()}
        requests.put(url, data = myobj)

        Client_confirm = Toplevel(AddClient_Screen)
        Client_confirm.title('Potwierdzenie')         

        #Labels
        
        Label(Client_confirm, text="Profil klienta został zaktualizowany", font=('Calibri',14, "bold italic")).grid(row=0,sticky=N,pady=20, padx=10)
        Button(Client_confirm , text='Zamknij', font=('Calibri', 12),width=8, command=  lambda: client_confirm_update(AddClient_Screen, Client_confirm)).grid(row=8, sticky=N, pady=5)
        Client_Screen.destroy()


    def OnDoubleClick(event):
        
        item = treeview.selection()
        kev = []
        for i in item:
           value = treeview.item(i, "values")

        #Vars
        temp_name = StringVar()
        temp_name.set(value[1])
        
        temp_tel = StringVar()
        temp_tel.set(value[2])
        
        temp_id = StringVar()
        temp_id.set(value[3])

        temp_city = StringVar()
        temp_city.set(value[4])

        temp_pcode = StringVar()
        temp_pcode.set(value[5])

        temp_street = StringVar()
        temp_street.set(value[6])

        temp_number = StringVar()
        temp_number.set(value[7])

        #AddClientScreen
        AddClient_Screen = Toplevel(master)
        AddClient_Screen.title('Add Client')

        #Labels
        Label(AddClient_Screen, text="Wprowadź dane klienta, aby dodać do systemu", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
        Label(AddClient_Screen, text="Imie i Nazwisko", font=('Calibri',12)).grid(row=1,sticky=W)
        Label(AddClient_Screen, text="Telefon", font=('Calibri',12)).grid(row=2,sticky=W)
        Label(AddClient_Screen, text="Numer Dowodu", font=('Calibri',12)).grid(row=3,sticky=W)
        Label(AddClient_Screen, text="Miasto", font=('Calibri',12)).grid(row=4,sticky=W)
        Label(AddClient_Screen, text="Kod Pocztowy", font=('Calibri',12)).grid(row=5,sticky=W)
        Label(AddClient_Screen, text="Ulica", font=('Calibri',12)).grid(row=6,sticky=W)
        Label(AddClient_Screen, text="Numer Domu", font=('Calibri',12)).grid(row=7,sticky=W)
        notif = Label(AddClient_Screen, font=('Calibri', 12))
        notif.grid(row=8, sticky=N, pady = 10)

        #Entries
        Entry(AddClient_Screen, textvariable=temp_name).grid(row=1, column=0)
        Entry(AddClient_Screen, textvariable=temp_tel).grid(row=2, column=0)
        Entry(AddClient_Screen, textvariable=temp_id).grid(row=3, column=0)
        Entry(AddClient_Screen, textvariable=temp_city).grid(row=4, column=0)
        Entry(AddClient_Screen, textvariable=temp_pcode).grid(row=5, column=0)
        Entry(AddClient_Screen, textvariable=temp_street).grid(row=6, column=0)
        Entry(AddClient_Screen, textvariable=temp_number).grid(row=7, column=0)

        #Buttons
        Button(AddClient_Screen, text='Zapisz', font=('Calibri', 12),width=8, command= lambda: update_client(temp_name, temp_tel, temp_id, temp_city, temp_pcode, temp_street, temp_number, value, notif, AddClient_Screen)).grid(row=9, sticky=N, pady=5)

    #ClientViewScreen
    global Client_Screen
    Client_Screen = Toplevel(master)
    Client_Screen.title('Active Rentals')                

    response = requests.get('http://127.0.0.1:8000/clients/')
    parsed = json.loads(response.text)
    Label(Client_Screen, text="Aktualna lista użytkowników w systemie", font=('Calibri',12)).grid(row=17,sticky=N)

    treeview = ttk.Treeview(Client_Screen, show="headings", columns=('ID', 'Imie i Nazwisko', 'Telefon', 'Numer Dowodu', 'Miasto', 'Kod pocztowy','Ulica', 'Numer domu'))
    treeview.heading("#1", text="ID")
    treeview.column("#1", minwidth=0, width=20, stretch=NO)
    treeview.heading("#2", text="Imie i nazwisko")
    treeview.column("#2", minwidth=0, width=100, stretch=NO)
    treeview.heading("#3", text="Telefon")
    treeview.column("#3", minwidth=0, width=100, stretch=NO)
    treeview.heading("#4", text="Numer Dowodu")
    treeview.column("#4", minwidth=0, width=100, stretch=NO)
    treeview.heading("#5", text="Miasto")
    treeview.column("#5", minwidth=0, width=100, stretch=NO)
    treeview.heading("#6", text="Kod Pocztowy")
    treeview.column("#6", minwidth=0, width=100, stretch=NO)
    treeview.heading("#7", text="Ulica")
    treeview.column("#7", minwidth=0, width=100, stretch=NO)
    treeview.heading("#8", text="Numer Domu")
    treeview.column("#8", minwidth=0, width=100, stretch=NO)
    treeview.grid()

    for row in parsed:
        treeview.insert("", "end", values=(row["id"], row["name"], row["tel"], row["personal_number"], row["city"], row["zip_code"], row["street"], row["house_number"]))
        treeview.bind("<Double-1>", OnDoubleClick)

    

# --------------------------------------------------------------------- ROWER ----------------------------------------------------------------------------------------------------------------------

def bike_view():
    
    def update_bike(temp_bike_id_number, temp_producer, temp_model, value, AddBike_Screen, notif):
        
        url = 'http://127.0.0.1:8000/bikes/'+value[0]+'/'
        myobj = {"bike_id_number": temp_bike_id_number.get(),"producer": temp_producer.get(),"model": temp_model.get()}

        
        if temp_bike_id_number.get() == "" or temp_producer.get() == "" or temp_model.get() == "":
            notif.config(fg="red", text="* Wszystkie pola są wymagane")
            return

        print(myobj)
        requests.put(url, json = myobj, headers = {'Content-Type': 'application/json'})


        Bike_confirm = Toplevel(AddBike_Screen)
        Bike_confirm.title('Potwierdzenie')         

        #Labels
        
        Label(Bike_confirm, text="Informacje o rowerze zostały zaktualizowane", font=('Calibri',14, "bold italic")).grid(row=0,sticky=N,pady=20, padx=10)
        Button(Bike_confirm , text='Zamknij', font=('Calibri', 12),width=8, command=  lambda: bike_confirm_update(AddBike_Screen, Bike_confirm)).grid(row=8, sticky=N, pady=5)
        Bike_Screen.destroy()
    
    def OnDoubleClick(event):

        item = treeview.selection()
        kev = []
        for i in item:
           value = treeview.item(i, "values")

        #Vars
        temp_bike_id_number = StringVar()
        temp_bike_id_number.set(value[1])
        
        temp_producer = StringVar()
        temp_producer.set(value[2])
        
        temp_model = StringVar()
        temp_model.set(value[3])

        #AddClientScreen
        AddBike_Screen = Toplevel(master)
        AddBike_Screen.title('Add Bike')

        #Labels
        Label(AddBike_Screen, text="Wprowadź dane roweru, aby edytować", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
        Label(AddBike_Screen, text="Numer ramy", font=('Calibri',12)).grid(row=1,sticky=W)
        Label(AddBike_Screen, text="Producent", font=('Calibri',12)).grid(row=2,sticky=W)
        Label(AddBike_Screen, text="Model", font=('Calibri',12)).grid(row=3,sticky=W)
        notif = Label(AddBike_Screen, font=('Calibri', 12))
        notif.grid(row=4, sticky=N, pady = 10)

        #Entries
        Entry(AddBike_Screen, textvariable=temp_bike_id_number).grid(row=1, column=0)
        Entry(AddBike_Screen, textvariable=temp_producer).grid(row=2, column=0)
        Entry(AddBike_Screen, textvariable=temp_model).grid(row=3, column=0)

        #Buttons
        Button(AddBike_Screen, text='Zapisz', font=('Calibri', 12),width=8, command= lambda: update_bike(temp_bike_id_number, temp_producer, temp_model, value, AddBike_Screen, notif)).grid(row=5, sticky=N, pady=5)

    #BikeViewScreen
    Bike_Screen = Toplevel(master)
    Bike_Screen.title('Active Rentals')                

    response = requests.get('http://127.0.0.1:8000/bikes/')
    parsed = json.loads(response.text)
    Label(Bike_Screen, text="Aktualna lista rowerów w systemie", font=('Calibri',12)).grid(row=17,sticky=N)

    treeview = ttk.Treeview(Bike_Screen, show="headings", columns=('ID', 'Numer ramy', 'Producent', 'Model', 'Dodano'))
    treeview.heading("#1", text="ID")
    treeview.column("#1", minwidth=0, width=20, stretch=NO)
    treeview.heading("#2", text="Numer Ramy")
    treeview.column("#2", minwidth=0, width=100, stretch=NO)
    treeview.heading("#3", text="Producent")
    treeview.column("#3", minwidth=0, width=100, stretch=NO)
    treeview.heading("#4", text="Model")
    treeview.column("#4", minwidth=0, width=100, stretch=NO)
    treeview.heading("#5", text="Dodano")
    treeview.column("#5", minwidth=0, width=100, stretch=NO)
    treeview.grid()

    for row in parsed:
        treeview.insert("", "end", values=(row["id"], row["bike_id_number"], row["producer"], row["model"], row["created"]))
        treeview.bind("<Double-1>", OnDoubleClick)

def create_bike(temp_bike_id_number, temp_producer, temp_model, notif, AddBike_Screen):
    url = 'http://127.0.0.1:8000/bikes/'
    myobj = {
            "bike_id_number": temp_bike_id_number.get(),
            "producer": temp_producer.get(),
            "model": temp_model.get(),
            "available": True
             }

    if temp_bike_id_number.get() == "" or temp_producer.get() == "" or temp_model.get() == "":
            notif.config(fg="red", text="* Wszystkie pola są wymagane")
            return
    requests.post(url, data = myobj)

    Bike_confirm = Toplevel(AddBike_Screen)
    Bike_confirm.title('Potwierdzenie')         

    #Labels        
    Label(Bike_confirm, text="Rower został dodany do systemu", font=('Calibri',14, "bold italic")).grid(row=0,sticky=N,pady=20, padx=10)
    Button(Bike_confirm , text='Zamknij', font=('Calibri', 12),width=8, command=  lambda: bike_confirm_create(AddBike_Screen, Bike_confirm)).grid(row=8, sticky=N, pady=5)

def add_bike():

    #Vars
    temp_bike_id_number = StringVar()
    temp_producer = StringVar()
    temp_model = StringVar()

    #AddClientScreen
    AddBike_Screen = Toplevel(master)
    AddBike_Screen.title('Add Bike')

    #Labels
    Label(AddBike_Screen, text="Wprowadź dane roweru, aby dodać do systemu", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
    Label(AddBike_Screen, text="Numer ramy", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(AddBike_Screen, text="Producent", font=('Calibri',12)).grid(row=2,sticky=W)
    Label(AddBike_Screen, text="Model", font=('Calibri',12)).grid(row=3,sticky=W)
    notif = Label(AddBike_Screen, font=('Calibri', 12))
    notif.grid(row=4, sticky=N, pady = 10)

    #Entries
    Entry(AddBike_Screen, textvariable=temp_bike_id_number).grid(row=1, column=0)
    Entry(AddBike_Screen, textvariable=temp_producer).grid(row=2, column=0)
    Entry(AddBike_Screen, textvariable=temp_model).grid(row=3, column=0)

    #Buttons
    Button(AddBike_Screen, text='Zapisz', font=('Calibri', 12),width=8, command=lambda: create_bike(temp_bike_id_number, temp_producer, temp_model, notif, AddBike_Screen)).grid(row=5, sticky=N, pady=5)

def bike_confirm_create(AddBike_Screen, Bike_confirm):
    
    Bike_confirm.destroy()
    AddBike_Screen.destroy()

def bike_confirm_update(AddBike_Screen, Bike_confirm):
    
    Bike_confirm.destroy()
    AddBike_Screen.destroy()
    bike_view()

#Image import
img = Image.open('bike.png')
img = img.resize((280,150))
img = ImageTk.PhotoImage(img)

#Labels
Label(master, text='Wypożyczalnia rowerów', font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
Label(master, text='Witaj w panelu administratora', font=('Calibri', 12)).grid(row=1, sticky=N, pady=10)
Button(master, text='Aktywne wypożyczenia', font=('Calibri', 12),width=20, command=rental_view).grid(row=2, column=0, sticky=N, pady=5)
Button(master, text='Dodaj wypożyczenie', font=('Calibri', 12),width=20, command= rental_create).grid(row=3,sticky=N, pady=5)
Label(master, image=img).grid(row=4, sticky=N, pady=15)

#Buttons
Button(master, text='Dodaj użytkownika', font=('Calibri', 12),width=20, command=add_client).grid(row=5, sticky=N, pady=5)
Button(master, text='Wyświetl użytkowników', font=('Calibri', 12),width=20, command=client_view).grid(row=6, sticky=N, pady=5)
Button(master, text='Dodaj rower', font=('Calibri', 12),width=20, command=add_bike).grid(row=7,sticky=N, pady=5)
Button(master, text='Wyświetl rowery', font=('Calibri', 12),width=20, command=bike_view).grid(row=8,sticky=N, pady=5)



