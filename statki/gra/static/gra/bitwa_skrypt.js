let wybranePole = "";

document.querySelectorAll('.pole').forEach(pole => {

    pole.addEventListener('click', () => {
        const poleID = pole.id;

        if (wybranePole == poleID) {
            wybranePole = "";
            pole.classList.remove('polePomaranczowe');
        } else {
            const usunietePole = document.getElementById(wybranePole);
            if (usunietePole) {
                usunietePole.classList.remove('polePomaranczowe');
            }
            wybranePole = pole.id;
            pole.classList.add('polePomaranczowe');
        }
    });
});


document.getElementById('strzel').addEventListener('click', () => {
     document.getElementById('wybrane_pole').value = wybranePole;
     document.getElementById('form').submit();
});