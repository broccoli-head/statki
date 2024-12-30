let wybranePole = "";

document.querySelectorAll('.pole').forEach(pole => {

    pole.addEventListener('click', () => {
        const poleID = pole.id;

        if (wybranePole == poleID) {
            wybranePole = "";
            pole.classList.remove('zaznaczone');
        } else {
            document.getElementById(wybranePole).classList.remove('zaznaczone');
            wybranePole = pole.id;
            pole.classList.add('zaznaczone');
        }
    });
});


// document.getElementById('strzel').addEventListener('click', () => {
//     document.getElementById('wybrane_pole').value = wybranePole;
//     document.getElementById('form').submit();
// });