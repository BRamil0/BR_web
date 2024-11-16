const navMenuButton = document.getElementsByClassName('nav-menu-button')
const navMenu = document.getElementById('nav-menu')


for (let i = 0; i < navMenuButton.length; i++) {
    navMenuButton[i].addEventListener('click', function() {
        if (navMenu.classList.contains('show')) {
            navMenu.classList.remove('show');
        } else {
            navMenu.classList.add('show');
        }
    });
}

document.addEventListener('click', function(event) {
    if (!navMenu.contains(event.target) && !isCheckingButton(navMenuButton, event)) {
        navMenu.classList.remove('show');
    }
});