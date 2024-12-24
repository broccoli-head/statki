from django.shortcuts import render
from .models import Uklad
from .NowaGra import NowaGra
import json


def lista(request):
    return render(request, "gra/lista.html")


def nowa_gra(request):
    komunikat = None
    gra = NowaGra();
    
    if request.method == 'POST':

        wybrane_pola = request.POST.get('wybrane_pola')
        wybrane_pola = json.loads(wybrane_pola)

        if not wybrane_pola:
            komunikat = "Nie wybrano żadnych pól!"
        else:
            try:
                wynik = gra.sprawdzanie_statkow(wybrane_pola)

                if wynik == True:
                    print(f"Poprawne pola: {wybrane_pola}")
                    Uklad.objects.create(pola = json.dumps(wybrane_pola))   #zapis do bazy danych
                    komunikat = "Wysłano dane do bazy!"

                else:
                    komunikat = wynik

            except ValueError as e:
                komunikat = str(e)
    
    context = {
        'liczby': range(10),
        'komunikat': komunikat
    }

    return render(request, "gra/nowa.html", context)