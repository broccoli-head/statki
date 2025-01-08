from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Gra(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'gry')
    ilosc_planszy = models.IntegerField(default = 0)
    data_rozpoczecia = models.DateTimeField(default = now)
    kolej_gracza = models.IntegerField(default = 0)
    komunikat = models.CharField(max_length = 128)
    #status 0 → gra trwa | status 1 → gracz 1 wygrał | status 2 → gracz 2 wygrał
    status = models.SmallIntegerField(default = 0)

    def __str__(self):
        return f"Gra {self.id}"

class Uklad(models.Model):
    gra = models.ForeignKey(Gra, on_delete=models.CASCADE, related_name="uklady")
    pola = models.CharField(max_length = 256)
    nietrafione = models.TextField()
    trafione = models.TextField()
    zatopione = models.TextField()