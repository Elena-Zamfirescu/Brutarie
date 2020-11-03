import gspread
from oauth2client.service_account import ServiceAccountCredentials
from functions import verificare_materie_prima
from functions import adaugare_materie_prima
from functions import eliminare_angajat
from functions import productie
scope = ['https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
googleClient = gspread.authorize(creds)
magazie = googleClient.open("Brutarie").worksheet("Magazie")
angajati = googleClient.open("Brutarie").worksheet("Angajati")
produse = googleClient.open("Brutarie").worksheet("Produse")

meniu=["Adaugare angajat","Elimare angajat","Afisare ingrediente disponibile","Adaugare/eliminare ingrediente","Productie", "Exit"]
while True:
    for option in meniu:
        print(f"{meniu.index(option)+1}. {option}")
    try:
        optiune = int(input("Selectati o optiune!\n>"))
        if optiune == 1:
            angajati.append_row([input("Nume:\n>"),input("Prenume:\n>"),input("Functie:\n>")])
            print("Angajatul a fost adaugat.")
        if optiune ==2:
            eliminare_angajat()
        elif optiune ==3:
            verificare_materie_prima()
        elif optiune ==4:
            adaugare_materie_prima()
        elif optiune ==5:
            productie()
        elif optiune ==6:
            break
        else:
            print("Optiunea nu este valida.")
    except ValueError:
        print("Optiunea nu este valida.")
