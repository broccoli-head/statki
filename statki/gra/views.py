from django.shortcuts import render
import json

def lista(request):
    return render(request, "gra/lista.html")

def nowa_gra(request):

    if request.method == 'POST':
        wybrane_pola = request.POST.get('wybrane_pola')
        if wybrane_pola:
            wybrane_pola = json.loads(wybrane_pola)     # zmiana z jsona na listę
            print(f"Zaznaczone pola: {wybrane_pola}")
    
    context = {
        'liczby': range(10)     # lista liczb od 0 do 9 - aby wygenerować tabelę 10x10 
    }

    return render(request, "gra/nowa.html", context)