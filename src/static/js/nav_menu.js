const menuNavToggle = document.getElementsByClassName('more-button')
const navMenu = document.getElementById('nav-menu')


let canClickButtonMenu = true;
for (let i = 0; i < menuNavToggle.length; i++) {
    menuNavToggle[i].addEventListener('click', function() {
        if (!canClickButtonMenu) return;
        canClickButtonMenu = false;
        navMenu.classList.toggle('show');
        setTimeout(function() {
            canClickButtonMenu = true;
        }, 150);
    })
}

document.addEventListener('click', function(event) {
    if (!navMenu.contains(event.target) && !isCheckingButton(menuNavToggle, event)) {
        navMenu.classList.remove('show');
    }
});