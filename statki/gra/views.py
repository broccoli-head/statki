from django.shortcuts import render
import json
import re


def lista(request):
    return render(request, "gra/lista.html")


def nowa_gra(request):
    komunikat = None
    
    if request.method == 'POST':

        wybrane_pola = request.POST.get('wybrane_pola')
        if wybrane_pola:
            wybrane_pola = json.loads(wybrane_pola)

            wartosc = sprawdzanie_statkow(wybrane_pola)
            if wartosc == True:
                print(f"Poprawne pola: {wybrane_pola}")
            else:
                komunikat = wartosc

        else:
            komunikat = "Nie wybrano żadnych pól!"
    
    context = {
        'liczby': range(10),
        'komunikat': komunikat
    }

    return render(request, "gra/nowa.html", context)



def sprawdzanie_statkow(wybrane_pola):
    
    tablica = [[0 for _ in range(10)] for _ in range(10)]   #tablica 10x10

    for pole in wybrane_pola:
        pozycja = re.search(r"(\d)x(\d)", pole)    #regex (0-9 x 0-9)
        if not pozycja:
            return "Niepoprawny format danych!"
        
        x, y = map(int, pozycja.groups())
        if 0 <= x < 10 and 0 <= y < 10:
            tablica[x][y] = True
        else:
            return "Pole poza zakresem planszy!"
    

    statki = znajdz_statki(tablica)
    dlugosci_statkow = [len(statek) for statek in statki]   #tablica przechowująca długości statków
    
    if any(dlugosc > 4 for dlugosc in dlugosci_statkow):
        return "Statki muszą być długości 1-4 kratek!"
    

    #lista kombinacji → →  DŁUGOŚĆ STATKU : ILOŚĆ STATKÓW
    kombinacje = {4: 1, 3: 2, 2: 3, 1: 4}

    for dlugosc, ilosc in kombinacje.items():
        if dlugosci_statkow.count(dlugosc) != ilosc:
            return "Niepoprawna kombinacja statków!"
    
    return True



def znajdz_statki(tablica):

    statki = []
    sprawdzone_pola = [[False for _ in range(10)] for _ in range(10)]   #tabela 10x10 wypełniona falsami

    def sprawdz(x, y, obecny_statek):

        if x < 0 or x >= 10 or y < 0 or y >= 10 or sprawdzone_pola[x][y] or tablica[x][y] == 0:
            return
        
        sprawdzone_pola[x][y] = True
        obecny_statek.append((x, y))

        #sprawdzenie pól sąsiadujących po bokach
        sprawdz(x+1, y, obecny_statek)
        sprawdz(x-1, y, obecny_statek)
        sprawdz(x, y+1, obecny_statek)
        sprawdz(x, y-1, obecny_statek)

        #sprawdzenie pól sąsiadujących na ukos
        sprawdz(x+1, y+1, obecny_statek)
        sprawdz(x+1, y-1, obecny_statek)
        sprawdz(x-1, y+1, obecny_statek)
        sprawdz(x-1, y-1, obecny_statek)


    for i in range(10):
        for j in range(10):
            if tablica[i][j] == True and not sprawdzone_pola[i][j]:
                obecny_statek = []
                sprawdz(i, j, obecny_statek, )
                statki.append(obecny_statek)
    
    for statek in statki:
        if not czy_liniowy(statek):
            return "Statki muszą być ułożone poziomo lub pionowo!"
    
    return statki


def czy_liniowy(statek):
    #tablica_x/y to zbiór wszystkich x i y aby ustalić czy statek jest pionowy lub poziomy 
    tablica_x = [x for x, y in statek]
    tablica_y = [y for x, y in statek]

    #set(tablica_x/y) usuwa powtórzenia - więc jeśli wszystkie x lub y są takie same, długość setu wynosi 1.
    #gdy długość = 1, oznacza to że statek jest poziomy/pionowy
    return len(set(tablica_x)) == 1 or len(set(tablica_y)) == 1