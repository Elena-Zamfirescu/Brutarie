import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
googleClient = gspread.authorize(creds)
magazie = googleClient.open("Brutarie").worksheet("Magazie")
angajati = googleClient.open("Brutarie").worksheet("Angajati")
produse_finale = googleClient.open("Brutarie").worksheet("Produse")


def verificare_materie_prima():
    produse=(magazie.col_values(1))
    cant = (magazie.col_values(2))
    um=(magazie.col_values(3))
    i=1
    print("*"*30)
    print("Produsele disponibile in magazie sunt:")
    while i<len(produse):
        print(f"{i}. {produse[i]}: {cant[i]} {um[i]}\n")
        i+=1
    print("*"*30)

def adaugare_materie_prima():
    while True:
        try:
            optiune=int(input("1. Adaugare materie prima noua\n2. Adaugare cantitate suplimenatra pentru o materie prima existenta\n3. Elimare materie prima din gestiune\n4. Exit\n>"))
            if optiune==1:
                magazie.append_row([input("Materie prima:\n>"), input("Cantitate:\n>"), input("unitate de masura:\n>")])
        except:
            print("Optiunea nu este valida")
        if optiune == 4:
            break
        if optiune ==2:
            materie = (magazie.col_values(1))
            cant = (magazie.col_values(2))
            um = (magazie.col_values(3))
            i=1
            while i < len(materie):
                print(f"{i}. {materie[i]}")
                i+=1
            try:
                de_adaugat=int(input("Selectati numarul corespunzator materiei prime pe care doriti sa o introduceti\n>"))

                cantitate=float(input(f"Introduceti cantitatea de adaugat in {um[de_adaugat]}.\n"))
            except:
                print("Optiunea nu este valida.")
            magazie.update_cell(de_adaugat+1, 2, (float(cant[de_adaugat])+cantitate))
            print("Cantitatea a fost introdusa")
        if optiune ==3:
            materie = (magazie.col_values(1))
            cant = (magazie.col_values(2))
            um = (magazie.col_values(3))
            i=1
            while i < len(materie):
                print(f"{i}. {materie[i]}")
                i+=1
            de_eliminat=int(input("Selectati numarul corespunzator materiei prime pe care doriti sa o scoateti din gestiune\n>"))
            print(f"Cantitatea disponibila este de {cant[de_eliminat]} {um[de_eliminat]}.")
            cantitate1=float(input(f"Ce cantitate doriti sa scadeti(in {um[de_eliminat]})?\n"))
            magazie.update_cell(de_eliminat+1, 2, (float(cant[de_eliminat])-cantitate1))
            print("Cantitatea a fost scoase din gestiune")


def eliminare_angajat():
    angajati = googleClient.open("Brutarie").worksheet("Angajati")
    Nume = (angajati.col_values(1))
    Prenume=(angajati.col_values(2))
    i=1
    while i<len(Nume):
        print(f"{i}. {Nume[i]} {Prenume[i]} ")
        i+=1
    de_eliminat = int(input("Selectati numarul corespunzator angajatului pe care doriti sa il eliminati\n>"))
    angajati.delete_rows(de_eliminat+1)
    print("Angajatul a fost eliminat")

def productie():
    produse=(magazie.col_values(1))
    cant = (magazie.col_values(2))
    um=(magazie.col_values(3))
    meniu=["Paine integrala","Covrigi cu susan","Chifle"]
    for produs in meniu:
        print(f"{meniu.index(produs) + 1}. {produs}")
    print("0. Exit")
    optiune=int(input("Selectati numarul corespunzator bakery-ului pe care doriti sa il produceti.\n>"))
    try:
        if optiune==1:
            print(f"Aveti nevoie de Lapte - 0.2l, Faina-0.3 kg, Drojdie - 0.05 kg")
            lapte = magazie.find("Lapte")
            faina = magazie.find("Faina")
            drojdie = magazie.find("Drojdie")
            maxim_produse=min(round(float(magazie.cell(lapte.row,2).value)/0.2),round(float(magazie.cell(faina.row,2).value)/0.3),round(float(magazie.cell(drojdie.row,2).value)/0.05))
            productie=int(input(f"Cate paini integrale doriti sa produceti, maximul este de {maxim_produse} produse.\n>"))
            magazie.update_cell(lapte.row,2, float(magazie.cell(lapte.row,2).value)-0.2*productie)
            magazie.update_cell(faina.row, 2, float(magazie.cell(faina.row, 2).value) - 0.3 * productie)
            magazie.update_cell(drojdie.row, 2, float(magazie.cell(drojdie.row, 2).value) - 0.05 * productie)
            paine=produse_finale.find("Paine integrala")
            produse_finale.update_cell(paine.row,2, int(produse_finale.cell(paine.row, 2).value)+productie)
            print("Productie finalizata cu succes.")
    except:
        print("Optiunea nu este valida")

    if optiune == 2:
        print(f"Aveti nevoie de Lapte - 0.15l, Faina-0.2 kg, Drojdie - 0.03 kg, Seminte susan - 15 grame")
        lapte = magazie.find("Lapte")
        faina = magazie.find("Faina")
        drojdie = magazie.find("Drojdie")
        seminte_susan=magazie.find("Seminte susan")
        maxim_produse = min(round(float(magazie.cell(lapte.row, 2).value) / 0.15),
                            round(float(magazie.cell(faina.row, 2).value) / 0.2),
                            round(float(magazie.cell(drojdie.row, 2).value) / 0.03),
                            round(float(magazie.cell(seminte_susan.row, 2).value) / 10))
        productie = int(input(f"Cati covrigi cu susan doriti sa produceti, maximul este de {maxim_produse} produse.\n>"))

        magazie.update_cell(lapte.row, 2, float(magazie.cell(lapte.row, 2).value) - 0.15 * productie)
        magazie.update_cell(faina.row, 2, float(magazie.cell(faina.row, 2).value) - 0.2 * productie)
        magazie.update_cell(drojdie.row, 2, float(magazie.cell(drojdie.row, 2).value) - 0.03 * productie)
        magazie.update_cell(seminte_susan.row, 2, float(magazie.cell(seminte_susan.row, 2).value) - 10 * productie)
        covrigi = produse_finale.find("Covrigi cu susan")
        produse_finale.update_cell(covrigi.row, 2, int(produse_finale.cell(covrigi.row, 2).value) + productie)
        print("Productie finalizata cu succes.")
    elif optiune == 3:
        print(f"Aveti nevoie de Lapte - 0.18l, Faina-0.25 kg, Drojdie - 0.03 kg, Seminte multi - 15 grame, Sare - 8 grame")
        lapte = magazie.find("Lapte")
        faina = magazie.find("Faina")
        drojdie = magazie.find("Drojdie")
        seminte_multi=magazie.find("Seminte multi")
        sare = magazie.find("Sare")
        maxim_produse = min(round(float(magazie.cell(lapte.row, 2).value) / 0.18),
                            round(float(magazie.cell(faina.row, 2).value) / 0.25),
                            round(float(magazie.cell(drojdie.row, 2).value) / 0.03),
                            round(float(magazie.cell(seminte_multi.row, 2).value) / 15),round(float(magazie.cell(sare.row, 2).value) / 8))
        productie = int(input(f"Cate chifle doriti sa produceti, maximul este de {maxim_produse} produse.\n>"))

        magazie.update_cell(lapte.row, 2, float(magazie.cell(lapte.row, 2).value) - 0.18 * productie)
        magazie.update_cell(faina.row, 2, float(magazie.cell(faina.row, 2).value) - 0.25 * productie)
        magazie.update_cell(drojdie.row, 2, float(magazie.cell(drojdie.row, 2).value) - 0.03 * productie)
        magazie.update_cell(seminte_multi.row, 2, float(magazie.cell(seminte_multi.row, 2).value) - 15 * productie)
        magazie.update_cell(sare.row, 2, float(magazie.cell(sare.row, 2).value) - 8 * productie)
        chifle = produse_finale.find("Chifle")
        produse_finale.update_cell(chifle.row, 2, int(produse_finale.cell(chifle.row, 2).value) + productie)
        print("Productie finalizata cu succes.")
    else:
        print(">Selectati o optiune valida.")
