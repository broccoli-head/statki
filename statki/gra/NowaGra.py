import re

class NowaGra:

    def __init__(self):
        #lista kombinacji → →  DŁUGOŚĆ STATKU : ILOŚĆ STATKÓW
        self.kombinacje = {4: 1, 3: 2, 2: 3, 1: 4}


    def sprawdzanie_statkow(self, wybrane_pola):    
        
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
        

        statki = self.znajdz_statki(tablica)
        dlugosci_statkow = [len(statek) for statek in statki]   #tablica przechowująca długości statków
        
        if any(dlugosc > 4 for dlugosc in dlugosci_statkow):
            return "Statki muszą być długości 1-4 kratek!"
        
        for dlugosc, ilosc in self.kombinacje.items():
            if dlugosci_statkow.count(dlugosc) != ilosc:
                return "Niepoprawna kombinacja statków!"
        
        return True



    def znajdz_statki(self, tablica):

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
            if not self.czy_liniowy(statek):
                raise ValueError("Statki muszą być ułożone poziomo lub pionowo!")   #rzuca wyjątek jako komunikat
        
        return statki


    def czy_liniowy(self, statek):
        #tablica_x/y to zbiór wszystkich x i y aby ustalić czy statek jest pionowy lub poziomy 
        tablica_x = [x for x, y in statek]
        tablica_y = [y for x, y in statek]

        #set(tablica_x/y) usuwa powtórzenia - więc jeśli wszystkie x lub y są takie same, długość setu wynosi 1.
        #gdy długość = 1, oznacza to że statek jest poziomy/pionowy
        return len(set(tablica_x)) == 1 or len(set(tablica_y)) == 1