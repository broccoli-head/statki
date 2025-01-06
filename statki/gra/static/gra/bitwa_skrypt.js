let wybranePole = "";

document.querySelectorAll('.plansze').forEach(plansza => {
    const trafione = plansza.getAttribute('trafione');
    const nietrafione = plansza.getAttribute('nietrafione');
    
    plansza.querySelectorAll('td').forEach(pole => {
        const numer = pole.textContent;
        const poleID = numer[0] + "x" + numer[1];

        if (trafione.search(poleID) != -1) {
            pole.classList.add('poleZielone');
            pole.classList.remove('pole');
        } else if (nietrafione.search(poleID) != -1) {
            pole.classList.add('poleCzerwone');
            pole.classList.remove('pole');
        }
    });
});


document.querySelectorAll('.pole').forEach(pole => {
    pole.addEventListener('click', () => {
        const poleID = pole.id;

        if (wybranePole === poleID) {
            wybranePole = "";
            pole.classList.remove('polePomaranczowe');
        } else {
            const usunietePole = document.getElementById(wybranePole);
            if (usunietePole) {
                usunietePole.classList.remove('polePomaranczowe');
            }
            wybranePole = poleID;
            pole.classList.add('polePomaranczowe');
        }
    });
});

document.getElementById('strzel').addEventListener('click', () => {
    if (wybranePole === "") {
        alert("Nie wybrano żadnych pól!");
        return;
    }
    document.getElementById('wybrane_pole').value = wybranePole;
    document.getElementById('form').submit();
});
