const navMenuButton = document.getElementsByClassName('nav-menu-button');
const navMenu = document.getElementById('nav-menu');

async function toggleNavMenu() {
    if (navMenu.classList.contains('show')) {
        navMenu.classList.remove('show');
    } else {
        navMenu.classList.add('show');
    }
}

Array.from(navMenuButton).forEach(button => {
    button.addEventListener('click', async function () {
        await toggleNavMenu();
    });
});

document.addEventListener('click', async function (event) {
    if (!navMenu.contains(event.target) && !await isCheckingButton(navMenuButton, event)) {
        navMenu.classList.remove('show');
    }
});