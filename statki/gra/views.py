from django.shortcuts import render
from .models import Gra, Uklad
from .NowaGra import NowaGra
import json


def lista(request):
    return render(request, "gra/lista.html")


def nowa_gra(request):

    komunikat = None
    blad = None
    ostatnia_gra = Gra.objects.last()

    if not ostatnia_gra or ostatnia_gra.ilosc_planszy == 2:
        obecny_gracz = 1
        gra = Gra.objects.create()

    elif ostatnia_gra.ilosc_planszy == 1:
        obecny_gracz = 2 
        gra = ostatnia_gra

    elif ostatnia_gra.ilosc_planszy == 0:
        obecny_gracz = 1
        gra = ostatnia_gra
    

    if request.method == 'POST':

        odpowiedz = request.POST.get('wybrane_pola')

        if (odpowiedz == "RESET"):
            gra.delete()
            obecny_gracz = 1

        else:
            wybrane_pola = json.loads(odpowiedz)
            if not wybrane_pola:
                blad = "Nie wybrano żadnych pól!"

            else:
                try:
                    plansza = NowaGra() 
                    wynik = plansza.sprawdzanie_statkow(wybrane_pola)

                    if wynik == True:
                        Uklad.objects.create(gra=gra, pola=json.dumps(wybrane_pola))    #zapisywanie do bazy danych
                        obecny_gracz += 1
                        gra.ilosc_planszy += 1
                        gra.save()

                        if (obecny_gracz > 2):
                            komunikat = None
                        else:
                            komunikat = f"Plansza gracza {obecny_gracz - 1} została zapisana!"

                    else:
                        blad = wynik

                except ValueError as e:
                    blad = str(e)
    

    context = {
        'wielkosc_planszy': range(10),
        'gracz': obecny_gracz,
        'komunikat': komunikat if not blad else blad,
        'kolor': "zielony" if not blad else "czerwony"
    }
        
    if obecny_gracz > 2:
        return render(request, "gra/bitwa.html", context)
    else:
        return render(request, "gra/nowa.html", context)


def bitwa(request):
    context = {
        'wielkosc_planszy': range(10)
    }
    
    return render (request, "gra/bitwa.html", context) 