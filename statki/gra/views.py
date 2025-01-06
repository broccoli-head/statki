from django.shortcuts import render, redirect
from .models import Gra, Uklad
from .NowaGra import NowaGra
import json, re, ast


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
    uklady = list(Uklad.objects.filter(gra=gra).order_by('id')[:2])
    trafione1 = uklady[0].trafione
    nietrafione1 = uklady[0].nietrafione
    trafione2 = uklady[1].trafione
    nietrafione2 = uklady[1].nietrafione

    context = {
        'wielkosc_planszy': range(10),
        'kolej': gra.kolej_gracza,
        'graID': gra.id,
        'komunikat': gra.komunikat,
        'kolor': "zielonaCzcionka" if gra.komunikat == "Trafiony!" else "czerwonaCzcionka",
        'trafione1': trafione1,
        'trafione2': trafione2,
        'nietrafione1': nietrafione1,
        'nietrafione2': nietrafione2
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
                if gra.kolej_gracza == 1:
                    atakowany_uklad = uklady[1]
                    uklad = uklady[0]
                    #jezeli nie ma pól, tworzy nową listę, a jeśli są to castuje stringa z polami do listy
                    listaTrafionych = [] if not trafione1 else ast.literal_eval(trafione1)
                    listaNietrafionych = [] if not nietrafione1 else ast.literal_eval(nietrafione1)
                else:
                    atakowany_uklad = uklady[0]
                    uklad = uklady[1]
                    listaTrafionych = [] if not trafione2 else ast.literal_eval(trafione2) 
                    listaNietrafionych = [] if not nietrafione2 else ast.literal_eval(nietrafione2)         

                if pole in listaTrafionych or pole in listaNietrafionych:
                    gra.komunikat = "Wybrano już to pole! Wybierz inne."
                else:
                    if pole in atakowany_uklad.pola:
                        gra.komunikat = "Trafiony!"
                        listaTrafionych.append(pole)
                        uklad.trafione = json.dumps(listaTrafionych)
                    else:
                        gra.komunikat = "Nie trafiłeś!"
                        listaNietrafionych.append(pole)
                        uklad.nietrafione = json.dumps(listaNietrafionych)
                    
                    uklad.save()
                    gra.kolej_gracza = 1 if gra.kolej_gracza == 2 else 2
                    
           
        gra.save()
        return redirect('gra:bitwa', gra_id=gra.id)
        
    else:
        return render (request, "gra/bitwa.html", context)   