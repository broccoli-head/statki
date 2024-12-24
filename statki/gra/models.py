from django.db import models

class Uklad(models.Model):
    nazwa = models.CharField(max_length = 30, unique = True, default = "Układ 1")
    pola = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.nazwa:
            numer = Uklad.objects.count() + 1
            self.nazwa = f"Układ {numer}"
        super(Uklad, self).save(*args, **kwargs)

    def __str__(self):
        return self.nazwa
 