from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Gra, Uklad
from .NowaGra import NowaGra
import json, re, ast


def rejestracja(request):
    if request.method == 'POST':
        formularz = UserCreationForm(request.POST)
        if formularz.is_valid():
            uzytkownik = formularz.save()
            login(request, uzytkownik)
            return redirect('gra:lista')
    else:
        formularz = UserCreationForm()

    return render(request, 'gra/rejestracja.html', {'form': formularz})


def zaloguj(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if not request.POST.get('zapamietaj'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(31536000)    #rok w sekundach
            return redirect('gra:lista')
    else:
        form = AuthenticationForm()
    return render(request, 'gra/login.html', {'form': form})


def wyloguj(request):
    logout(request)
    return redirect('gra:login')
    

@login_required(login_url = '/gra/login/')
def lista(request):
    gry = Gra.objects.filter(uzytkownik = request.user).order_by('-id')[:10]    #10 ostatnich gier
    return render(request, "gra/lista.html", {'gry': gry})



@login_required(login_url = '/gra/login/')
def nowa_gra(request):
    komunikat = None
    blad = None
    gra = None
    ostatnia_gra = Gra.objects.last()

    #ilosc planszy to inaczej liczba graczy, którzy już wybrali swoje pola
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
                            gra = Gra.objects.create(uzytkownik = request.user)

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


@login_required(login_url = '/gra/login/')
def bitwa(request, gra_id):
    gra = Gra.objects.get(id = gra_id)
    if gra.ilosc_planszy == 1:
        return redirect('gra:nowa_gra')

    if gra.uzytkownik != request.user:
        return HttpResponseForbidden("<p>Nie masz dostępu do tej gry.</p><a href='/gra'>Aby powrócić, kliknij tutaj</a>")
    
    uklady = list(Uklad.objects.filter(gra = gra).order_by('id')[:2])
  
    #musimy zdeklarować niestety wszystkie trafione, nietrafione i zatopione
    #aby wyświetlić dobre kolory pól dla obu graczy jednocześnie
    trafione1 = uklady[0].trafione
    nietrafione1 = uklady[0].nietrafione
    trafione2 = uklady[1].trafione
    nietrafione2 = uklady[1].nietrafione
    zatopione1 = uklady[0].zatopione
    zatopione2 = uklady[1].zatopione

    context = {
        'wielkosc_planszy': range(10),
        'kolej': gra.kolej_gracza,
        'graID': gra.id,
        'komunikat': gra.komunikat,
        'kolor': "zielonaCzcionka" if "Trafiony" in gra.komunikat else "czerwonaCzcionka",
        'trafione1': trafione1,
        'trafione2': trafione2,
        'nietrafione1': nietrafione1,
        'nietrafione2': nietrafione2,
        'zatopione1': zatopione1,
        'zatopione2': zatopione2,
        'status': gra.status
    }


    if gra.kolej_gracza == 0:
        return redirect("/gra/nowa/")

    if request.method == 'POST':
        odpowiedz = request.POST.get('wybrane_pole')
        wybrane_pole = re.search(r"(\d)x(\d)", odpowiedz)    #regex (0-9 x 0-9)

        if odpowiedz == "":
            gra.komunikat = "Nie wybrano żadnego pola!"
        elif not wybrane_pole:
            gra.komunikat = "Niepoprawny format danych!"
        else:
            x, y = map(int, wybrane_pole.groups())
            if not (0 <= x < 10 and 0 <= y < 10):
                gra.komunikat = "Pole poza zakresem planszy!"
            else:
                wybrane_pole = wybrane_pole.group(0)

                if gra.kolej_gracza == 1:
                    atakowany_uklad = uklady[1]
                    uklad = uklady[0]
                    #jezeli nie ma pól, tworzy nową listę, a jeśli są to castuje stringa z polami do listy
                    listaTrafionych = [] if not trafione1 else ast.literal_eval(trafione1)
                    listaNietrafionych = [] if not nietrafione1 else ast.literal_eval(nietrafione1)
                    listaZatopionych = [] if not zatopione1 else ast.literal_eval(zatopione1)

                else:
                    atakowany_uklad = uklady[0]
                    uklad = uklady[1]
                    listaTrafionych = [] if not trafione2 else ast.literal_eval(trafione2) 
                    listaNietrafionych = [] if not nietrafione2 else ast.literal_eval(nietrafione2)         
                    listaZatopionych = [] if not zatopione2 else ast.literal_eval(zatopione2)


                if wybrane_pole in listaTrafionych or wybrane_pole in listaNietrafionych or wybrane_pole in listaZatopionych:
                    gra.komunikat = "Wybrano już to pole! Wybierz inne."
                else:
                    if wybrane_pole in atakowany_uklad.pola:
                        listaTrafionych.append(wybrane_pole)
                        uklad.trafione = json.dumps(listaTrafionych)
                        
                        tablica = [[False for _ in range(10)] for _ in range(10)]   #tablica 10x10 wypełniona falsami
                        pozycje = json.loads(atakowany_uklad.pola)
                        for pozycja in pozycje:
                            x, y = map(int, pozycja.split('x'))
                            tablica[x][y] = True

                        plansza = NowaGra()
                        statki = plansza.znajdz_statki(tablica)

                        #pola statków zwracane są jako krotki np. (3, 4)
                        #dlatego zmieniamy ich format np. 3x4
                        for statek in statki:
                            statek = [f"{x}x{y}" for x, y in statek]
                            if wybrane_pole in statek:
                                statek_atakowany = statek     #statek atakowany to tablica pól statku, który został trafiony
                                break

                        #jezeli wszystkie pola statku atakowanego znajdują się w liście trafionych, jest on zatopiony
                        if all(pole in listaTrafionych for pole in statek_atakowany):
                            print(listaTrafionych, statek_atakowany)
                            gra.komunikat = "Trafiony, zatopiony!"

                            for pole in statek_atakowany:
                                if pole in listaTrafionych:
                                    listaTrafionych.remove(pole) 

                            listaZatopionych.append(statek_atakowany)
                            uklad.trafione = json.dumps(listaTrafionych)
                            uklad.zatopione = json.dumps(listaZatopionych)

                            if (len(listaZatopionych) == 10):
                                gra.status = gra.kolej_gracza

                        else:
                            gra.komunikat = "Trafiony!"

                    else:
                        gra.komunikat = "Nie trafiłeś!"
                        listaNietrafionych.append(wybrane_pole)
                        uklad.nietrafione = json.dumps(listaNietrafionych)
                    
                    uklad.save()
                    gra.kolej_gracza = 1 if gra.kolej_gracza == 2 else 2
                    
           
        gra.save()
        return redirect('gra:bitwa', gra_id=gra.id)
        
    else:
        return render (request, "gra/bitwa.html", context)   