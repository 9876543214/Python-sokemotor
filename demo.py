import os
import re
import sys
from colorama import init, Back, Style #Farger
import json
import pyautogui #Kan imitere brukerinput
import subprocess
import time

filepath = ("C:\\Users\\Ulrik\\Python\\Oppdrag søkemotor\\Tekstfiler") # Bytt til egen filvei
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
        input("Ugyldig valg. Trykk en tast for å prøve på nytt")
        start()

def velg_fil(tall):
    print(" ")
    print("Tiljengelige filer:")
    for file in dirlist:
        print(file)
    while True:
        valgtfil = input("Velg en fil: ")
        riktig_filnavn = False
        for file in dirlist: #sjekker om filnavn finnes
            if valgtfil == file:
                riktig_filnavn = True
        if riktig_filnavn == False:
            input("Fant ikke fil. Trykk en tast for å prøve på nytt.")
        elif riktig_filnavn == True:
            break
    if tall == "1":
        søk_i_fil(valgtfil)
    elif tall == "3":
        skriv_til_fil(valgtfil)
    else:
        input("Det skjedde en feil. Trykk en tast for å prøve igjen") #Hvis tall er udefinert
        start()

def søk_i_fil(filnavn): 
    while True:
        print(" ")
        print("Du kan søke etter tegn, ord eller setninger:")
        søk = input("Søk: ")
        if filnavn != None:
            finnsøk(søk, filnavn)
        else:
            for file in dirlist:
                finnsøk(søk, file)
        while True:
            print(" ")
            søk_igjen = input("Vil du søke igjen? Y/N: ")
            if søk_igjen == "N" or søk_igjen == "n" or søk_igjen == "Y" or søk_igjen == "y":
                break
            else:
                input("Ugyldig input. Trykk en tast for å prøve igjen.")
        if søk_igjen == "N" or søk_igjen == "n":
            break
    start()


def finnsøk(søk, filnavn):
    print(" ")
    print(Style.BRIGHT, filnavn, ":", Style.NORMAL)
    file_path = os.path.join(filepath, filnavn)
    treff = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()
        søkfunnet = False
        for row in lines:
            if row.find(søk) != -1:
                print(" ")
                print("Søk funnet på linje ", lines.index(row) + 1)
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


def skriv_til_fil(valgtfil):
    path = os.path.join(filepath, valgtfil)    
    f = open(path, "r") #Åpne fil som r for å lese antall linjer
    lines = f.readlines()
    wf = open(path, "a+") #Åpnet som a+ for å redigere og skrive nytt
    total_linjer = len(lines)
    total_linjer_str = json.dumps(total_linjer)  
    while True: #loop hvis brukerinput er feil
        print("Velg en linje fra 1-" + total_linjer_str + ", eller skriv \"N\" for ny linje", end="")# input kan ikke ha flere ledd, så måtte skrive ut som print først
        valgt_linje = input(": ")
        try:
            valgt_linje_int = int(valgt_linje) #sjekker om valgt linje kan bli int
        except ValueError:
            if valgt_linje == "n" or valgt_linje == "N": #for å skrive på ny linje
                print("Skriv inn på ny linje", total_linjer + 1, ":")
                nytekst = input("Skriv her: ")
                wf.write("\n" + nytekst)
                wf.flush()
                input("Tekst skrevet inn. Trykk en tast for å fortsette.")
                start()
                break
            else:
                input("Ugyldig input. Trykk en tast for å prøve på nytt")
                continue
        if 0 < valgt_linje_int <= total_linjer: # sjekker om valgt linje finnes
            endre_linje(valgt_linje_int, path)
            break
        else:
            print(" ")
            input("Nummer er utenfor rekkevidde. Trykk en tast for å prøve på nytt.")
        
def endre_linje(tall, filvei): #Funksjon for å endre linje som finnes
    f = open(filvei, "r")
    
    tekst = "None"
    print(" ")
    print("Rediger linje", tall, "under:")
    linjenr = 0
    linjer = f.readlines()
    for line in linjer:
        linjenr = linjenr + 1
        if linjenr == tall:
            tekst = line.strip()
            linjenr = 0
            break
    for char in tekst: #Skriver ut tekst en og en karakter, men kan ikke endres av bruker
        sys.stdout.write(char) 
        sys.stdout.flush()
        time.sleep(0.02)
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
    input("Linje redigert. Trykk en tast for å fortsette")
    start()


def lag_fil():
    print("Ikke tiljengelig")


start()