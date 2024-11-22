import os
import re
import sys
from colorama import Back, Style #Farger
import pyautogui #Kan imitere brukerinput
import time

filepath = ("C:\\Users\\Ulrik\\Python\\Oppdrag_sokemotor\\Tekstfiler") # Bytt til egen filvei
dirlist = os.listdir(filepath)

def start():
    print("-----------Søkemotor----------")
    print("| 1. Søk i en fil            |")
    print("| 2. Søk i alle filer        |")
    print("| 3. Skriv inn i fil         |")
    print("| 4. Lag ny fil              |")
    print("------------------------------")
    menyvalg = input("Velg tall 1-4 fra menyen: ")

    if menyvalg == "1":
        velg_fil(menyvalg)
    elif menyvalg == "2":
        none = None
        søk_i_fil(none)
    elif menyvalg == "3":
        velg_fil(menyvalg)
    elif menyvalg == "4":
        lag_fil()
    else:
        input("Ugyldig valg. Trykk enter for å prøve på nytt")
        start()

def velg_fil(tall):
    print(" ")
    print("Tiljengelige filer:")
    filenr = 0
    for file in dirlist:
        filenr = filenr + 1
        filenr_str = str(filenr)
        print(filenr_str + ". " + file) #Printer alle tiljengelige filer
    while True:
        
        print("Velg en fil fra 1-" + filenr_str, end="")
        valgtfiltall = input(": ")
        valgtfiltall_int = int(valgtfiltall)
        riktig_filnavn = False
        for file in dirlist:
            if file == dirlist[valgtfiltall_int - 1]:
                valgtfil = file
                riktig_filnavn = True
        if riktig_filnavn == False:
            input("Fant ikke fil. Trykk enter for å prøve på nytt.")
        elif riktig_filnavn == True:
            break #Hvis filnavn finnes, fortsetter funksjonen
    if tall == "1":
        søk_i_fil(valgtfil)
    elif tall == "3":
        skriv_til_fil(valgtfil)
    else:
        input("Det skjedde en feil. Trykk enter for å prøve igjen") #Hvis tall er udefinert
        start()

def søk_i_fil(filnavn): 
    while True:
        print(" ")
        print("Du kan søke etter tegn, ord eller setninger:")
        søk = input("Søk: ")
        if filnavn != None: #Hvis filnavn er valgt, kjører funksjonen kun en gang
            finnsøk(søk, filnavn)
        else: #Hvis filen ikke er valgt, kjører fungsjonen en gang per fil
            ferdig = 1
            totaltreff = 0
            for file in dirlist:
                treff = finnsøk(søk, file)
                totaltreff = treff + totaltreff #Finner totalen av antall treff i alle filer
                if ferdig == int(len(dirlist)):
                    print(" ")
                    print("Alle filer sjekket")
                    print("Totalt", totaltreff, "treff funnet i alle filer") #Printer totalt antall treff
                else:    
                    print(" ")
                    input("Trykk enter for neste fil.")
                    ferdig = ferdig + 1
        while True:
            print(" ")
            søk_igjen = input("Vil du søke igjen? Y/N: ")
            if søk_igjen == "N" or søk_igjen == "n" or søk_igjen == "Y" or søk_igjen == "y": #Sjekker om input er gyldig
                break
            else:
                input("Ugyldig input. Trykk enter for å prøve igjen.")
        if søk_igjen == "N" or søk_igjen == "n":
            break
    start()


def finnsøk(søk, filnavn):
    print(" ")
    print(Style.BRIGHT, filnavn, ":", Style.NORMAL) #skriver "fillnavn:" i bold tekst
    file_path = os.path.join(filepath, filnavn) #filvei
    treff = 0
    with open(file_path, 'r') as f:
        lines = f.readlines() #antall linjer i filen
        søkfunnet = False
        for row in lines:
            if row.find(søk) != -1:
                print(" ")
                print("Søk funnet på linje", lines.index(row) + 1)
                treff = treff + 1
                highlighted_row = re.sub(
                    f"({re.escape(søk)})",
                    Back.YELLOW + r"\1" + Style.RESET_ALL,
                    row.strip() 
                )
                print(highlighted_row)
                
                søkfunnet = True
        if søkfunnet == False:
                print(" ")
                print("Fant ikke søk i fil " + filnavn)
        else:
            print(" ")
            print(treff, "treff funnet i fil " + filnavn)
            return treff


def skriv_til_fil(valgtfil):
    path = os.path.join(filepath, valgtfil)    
    f = open(path, "r") #Åpne fil som r for å lese antall linjer
    lines = f.readlines()
    wf = open(path, "a+") #Åpnet som a+ for å redigere og skrive nytt
    total_linjer = len(lines)
    total_linjer_str = str(total_linjer)
    while True: #loop hvis brukerinput er feil
        print(valgtfil)
        print("Velg en linje fra 1-" + total_linjer_str + ", eller skriv \"N\" for ny linje", end="")# input kan ikke ha flere ledd, så måtte skrive ut som print først
        valgt_linje = input(": ")            
        if total_linjer == 0:
            print("Fil har ingen linje å redigere.")
            while True: 
                skriv_ny_linje = input("Vil du skrive inn på ny linje? Y/N: ")
                if skriv_ny_linje == "Y" or skriv_ny_linje == "y":
                    valgt_linje = "n"
                    break
                elif skriv_ny_linje == "n" or skriv_ny_linje == "N":
                    start()
                    break
                else:
                    input("Ugyldig input. Trykk enter for å fortsette")
        try:
            valgt_linje_int = int(valgt_linje) #sjekker om valgt linje kan bli int        

        except ValueError:
            if valgt_linje == "n" or valgt_linje == "N": #for å skrive på ny linje
                print("Skriv inn på ny linje", total_linjer + 1)
                nytekst = input("Skriv her: ")
                wf.write("\n" + nytekst)
                wf.flush()
                input("Tekst skrevet inn. Trykk enter for å fortsette.")
                while True:
                    print(" ")
                    skriv_igjen = input("Vil du skrive ny igjen? Y/N: ")
                    if skriv_igjen == "N" or skriv_igjen == "n":  #Sjekker om input er gyldig
                        start()
                        break
                    elif skriv_igjen == "Y" or skriv_igjen == "y":
                        skriv_til_fil(valgtfil)
                        break
                    else:
                        input("Ugyldig input. Trykk enter for å prøve igjen.")

                break
            else:
                input("Ugyldig input. Trykk enter for å prøve på nytt")
                continue


        if 0 < valgt_linje_int <= total_linjer: # sjekker om valgt linje finnes
            endre_linje(valgt_linje_int, path, valgtfil)
            break
        else:
            input("Nummer er utenfor rekkevidde. Trykk enter for å prøve på nytt.")
        


def endre_linje(tall, filvei, fil): #Funksjon for å endre linje som finnes
    f = open(filvei, "r")
    tekst = "None"
    print(" ")
    print("Rediger linje", tall, "under:")
    linjenr = 0
    linjer = f.readlines()
    for line in linjer:
        linjenr = linjenr + 1
        if linjenr == tall:
            tekst = line.strip() # Henter valgt linje
            linjenr = 0
            break
    for char in tekst: #Skriver ut tekst en og en karakter, men kan ikke endres av bruker
        sys.stdout.write(char) 
        sys.stdout.flush()
        time.sleep(0.04)
    sys.stdout.write('\r' + '' * len(tekst)) #Fjerner skrevet ut tekst
    sys.stdout.flush()
    pyautogui.typewrite(tekst) #skriver inn tekst igjen som bruker, så bruker kan endre
    #Jeg valgte å gjøre dette for at bruker skulle skjønne at teksten kunne redigeres, og det fungerte ikke med å skrive en og en karakter som brukerinput
    changedline = input("")
    for line in linjer:
        linjenr = linjenr + 1
        if linjenr == tall:
            wf = open(filvei, "w")
            linjer[tall - 1] = changedline + "\n"
            wf.writelines(linjer)
            wf.flush()
    print("Linje redigert.")
    while True:
        print(" ")
        rediger_igjen = input("Vil du redigere linje igjen? Y/N: ")
        if rediger_igjen == "N" or rediger_igjen == "n":  #Sjekker om input er gyldig
            start()
            break
        elif rediger_igjen == "Y" or rediger_igjen == "y":
            skriv_til_fil(fil)
        else:
            input("Ugyldig input. Trykk enter for å prøve igjen.")


def lag_fil():
    global dirlist
    while True:
        print(" ")
        print("Skriv kun filnavn, ikke med .")
        nyfilnavn = input("Hva vil du kalle filen? :")
        filtrert_filnavn = nyfilnavn.replace(" ", "-").replace(".", "-") #filtrerer filnavn
        try:
            f = open(filepath + "\\" + filtrert_filnavn + ".txt", 'x') #lager filen
            break
        except:
            print("Fil finnes allerede")
            input("Trykk enter for å prøve igjen.")
            continue
    print("Fil opprettet")
    dirlist = os.listdir(filepath)
    while True:
        opprett_igjen = input("Vil du opprette en til fil? Y/N: ")
        if opprett_igjen == "N" or opprett_igjen == "n":  #Sjekker om input er gyldig
            start()
            break
        elif opprett_igjen == "Y" or opprett_igjen == "y":
            lag_fil()
            break
        else:
            input("Ugyldig input. Trykk enter for å prøve igjen.")

    


start()