from django.shortcuts import render, redirect
from .models import Gra, Uklad
from .NowaGra import NowaGra
import json


def lista(request):
    gry = Gra.objects.all().order_by('-id')[:10]    #10 ostatnich gier
    context = {
        'gry': gry
    }
    return render(request, "gra/lista.html", context)


def nowa_gra(request):
    komunikat = None
    blad = None
    ostatnia_gra = Gra.objects.last()

    if not ostatnia_gra or ostatnia_gra.ilosc_planszy == 2:
        obecny_gracz = 1


    elif ostatnia_gra.ilosc_planszy == 1:
        obecny_gracz = 2 
        gra = ostatnia_gra

    else:
        obecny_gracz = 1
        gra = ostatnia_gra
    

    if request.method == 'POST':

        odpowiedz = request.POST.get('wybrane_pola')

        if (odpowiedz == "RESET"):
            if gra:
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
                        gra = Gra.objects.create()
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
        gra.kolej_gracza += 1
        gra.save()
        return redirect('gra:bitwa', gra_id = gra.id)
    else:
        return render(request, "gra/nowa.html", context)


def bitwa(request, gra_id):
    komunikat = None
    gra = Gra.objects.get(id = gra_id)
    kolej = gra.kolej_gracza
    uklady = Uklad.objects.filter(gra = gra).order_by('-id')[:2]
    
    context = {
        'wielkosc_planszy': range(10),
        'komunikat': komunikat,
        'kolej': kolej,
        'gra': gra,
        'uklady': uklady
    }

    if kolej == 0:
        return redirect("/gra/nowa/")
    elif kolej == 1:
        komunikat = "Graczu 1, wybierz pole i strzelaj!"
        return render (request, "gra/bitwa.html", context) 
    else:
        return render (request, "gra/bitwa.html", context) 