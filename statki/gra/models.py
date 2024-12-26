from django.db import models

class Gra(models.Model):
    ilosc_planszy = models.IntegerField(default = 0)
    data_rozpoczecia = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"Gra {self.id}"

class Uklad(models.Model):
    gra = models.ForeignKey(Gra, on_delete=models.CASCADE, related_name="uklady", null = True)
    pola = models.TextField()