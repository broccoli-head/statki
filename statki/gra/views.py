from django.shortcuts import render

# Create your views here.

def lista(request):
    return render(request, "gra/lista.html")

def nowa_gra(request):
    context = {
        'liczby': range(10)     # lista liczb od 0 do 9 - potrzebna aby wygenerować tabelę 10x10 
    }
    return render(request, "gra/nowa.html", context)