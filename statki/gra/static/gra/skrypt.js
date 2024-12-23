const wybranePola = new Set();


document.querySelectorAll('.pole').forEach(pole => {

    pole.addEventListener('click', () => {
        const poleID = pole.id;

        if (wybranePola.has(poleID)) {
            wybranePola.delete(poleID);
            pole.classList.remove('zaznaczone');
        } else {
            wybranePola.add(poleID);
            pole.classList.add('zaznaczone');
        }
    });

});


document.getElementById('potwierdz_plansze').addEventListener('click', () => {

    const tab = Array.from(wybranePola);
    document.getElementById('wybrane_pola').value = JSON.stringify(tab);
    document.getElementById('form').submit();

});