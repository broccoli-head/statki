let wybranePole = "";

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
