from django.db import models
from django.utils.timezone import now

class Gra(models.Model):
    ilosc_planszy = models.IntegerField(default = 0)
    data_rozpoczecia = models.DateTimeField(default = now)
    kolej_gracza = models.IntegerField(default = 0)
    komunikat = models.CharField(max_length = 128)

    def __str__(self):
        return f"Gra {self.id}"

class Uklad(models.Model):
    gra = models.ForeignKey(Gra, on_delete=models.CASCADE, related_name="uklady", null = True)
    pola = models.CharField(max_length = 256)
    trafione_pola = models.TextField()