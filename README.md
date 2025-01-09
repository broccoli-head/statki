# ==== 🚢 STATKI 🚢 ====
Prosta gra w okręty oparta na frameworku Django.

## 📖 OPIS I FUNKCJE 📖
1. Rejestracja i logowanie się z opcją zapamiętania użytkownika.
![Logowanie](gify/logowanie.gif)

2. Dla każdego konta jest osobna lista gier!

3. Tworzenie nowej gry polega na wybraniu pól przez obu graczy. Gra odbywa się **na pojedynczym komputerze**!!!

4. Podczas wybierania statków algorytm sprawdza:
- czy wybrano pola i czy format danych jest poprawny
- czy statki są w jednej linii 
- czy okręty nie dotykają się
- czy zgadza się ilość oraz długość statków
<br><br>
![Rozgrywka](gify/wybieranie.gif)
5. Bitwa polega na przemiennym strzelaniu w pola przeciwnika:
- jeśli dobrze trafisz, dalej jest twoja kolej
- pola trafione i nietrafione są oznaczone na zielono i czerwono
- statki zatopione są skreślone
- gra jest zaopatrzona w komunikaty błędów oraz informacje, czy statek został trafiony, nietrafiony lub zatopiony
<br><br>
![Bitwa](gify/rozgrywka.gif)
6. Wszystkie dane użytkowników oraz moment zatrzymania gry są zapisywane w bazie danych, więc bez obaw można wyłączyć stronę w dowolnym momencie i nawet na innym urządzeniu kontynuować grę.

## ❗ Kod jest pracą własną ❗
Użyte języki:
- Python + Django
- HTML
- JavaScript
- CSS