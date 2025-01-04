from django.shortcuts import render, redirect
from .models import Gra, Uklad
from .NowaGra import NowaGra
import json, re


def lista(request):
    gry = Gra.objects.all().order_by('-id')[:10]    #10 ostatnich gier
    context = {
        'gry': gry
    }
    return render(request, "gra/lista.html", context)


def nowa_gra(request):
    komunikat = None
    blad = None
    gra = None
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
                        if obecny_gracz == 1:
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
        'kolor': "zielonaCzcionka" if not blad else "czerwonaCzcionka"
    }
        
    if obecny_gracz > 2:
        gra.kolej_gracza += 1
        gra.save()
        return redirect('gra:bitwa', gra_id = gra.id)
    else:
        return render(request, "gra/nowa.html", context)



def bitwa(request, gra_id):
    gra = Gra.objects.get(id = gra_id)
    uklady = Uklad.objects.filter(gra = gra).order_by('id')[:2]
    
    context = {
        'wielkosc_planszy': range(10),
        'kolej': gra.kolej_gracza,
        'graID': gra.id,
        'komunikat': gra.komunikat,
        'kolor': "zielonaCzcionka" if gra.komunikat == "Trafiony!" else "czerwonaCzcionka",
        'trafione1': uklady[0].trafione_pola,
        'trafione2': uklady[1].trafione_pola
    }

    if gra.kolej_gracza == 0:
        return redirect("/gra/nowa/")

    if request.method == 'POST':
        odpowiedz = request.POST.get('wybrane_pole')
        pole = re.search(r"(\d)x(\d)", odpowiedz)    #regex (0-9 x 0-9)

        if odpowiedz == "":
            gra.komunikat = "Nie wybrano żadnego pola!"
        elif not pole:
            gra.komunikat = "Niepoprawny format danych!"
        else:
            x, y = map(int, pole.groups())
            if not (0 <= x < 10 and 0 <= y < 10):
                gra.komunikat = "Pole poza zakresem planszy!"
            else:
                pole = pole.group(0)

                atakowany_uklad = uklady[1] if gra.kolej_gracza == 1 else uklady[0]
                gra.kolej_gracza = 2 if gra.kolej_gracza == 1 else 1
                gra.komunikat = "Trafiony!" if pole in atakowany_uklad.pola else "Nie trafiłeś!"
                
        gra.save()
        return redirect('gra:bitwa', gra_id=gra.id)
        
    else:
        return render (request, "gra/bitwa.html", context)   