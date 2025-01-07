const wybranePola = new Set();

document.querySelectorAll('.pole').forEach(pole => {

    pole.addEventListener('click', () => {
        const poleID = pole.id;

        if (wybranePola.has(poleID)) {
            wybranePola.delete(poleID);
            pole.classList.remove('poleZielone');
        } else {
            wybranePola.add(poleID);
            pole.classList.add('poleZielone');
        }
    });
});


const nowa = document.getElementById('nowa');
const wyloguj = document.getElementById('wyloguj');
const potwierdzPlansze = document.getElementById('potwierdz_plansze');
const reset = document.getElementById('reset');
const powrot = document.getElementById('powrot');


if (nowa) nowa.addEventListener('click', () => location.href = '/gra/nowa');

if (wyloguj) wyloguj.addEventListener('click', () => { 
    if(confirm("Czy aby na pewno chcesz się wylogować?")) {
        location.href = '/gra/wyloguj';
    }
});

if (potwierdzPlansze) potwierdzPlansze.addEventListener('click', () => {
    const tab = Array.from(wybranePola);
    document.getElementById('wybrane_pola').value = JSON.stringify(tab);
    document.getElementById('form').submit();
});

if (reset) reset.addEventListener('click', () => {
    if (confirm("Spowoduje to zresetowanie planszy obu graczy. Kontynuuować?")) {
        document.getElementById('wybrane_pola').value = "RESET";
        document.getElementById('form').submit();
    }
});

if (powrot) powrot.addEventListener('click', () => location.href = '..');