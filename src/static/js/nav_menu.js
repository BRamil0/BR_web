const mobileNavMenu = document.querySelector('.nav-center')
const menuMobileNavToggle = document.getElementById('mobile-menu-toggle')
const navLinks = mobileNavMenu.querySelectorAll('.mobile-nav-link') // Select all nav link
const menuNavToggle = document.getElementById('more-button')
const navMenu = document.getElementById('nav-menu')


let canClickButtonMenu = true;
menuNavToggle.addEventListener('click', () => {
    if (!canClickButtonMenu) return;
    canClickButtonMenu = false;

    if (navMenu.classList.contains('show')) {
        navMenu.classList.remove('show');
        console.log("Клас .show видалений");
    } else {
        navMenu.classList.add('show');
        console.log("Клас .show доданий");
    }

    setTimeout(() => {
        canClickButtonMenu = true;
    }, 150);
});



document.addEventListener('click', function(event) {
    if (!navMenu.contains(event.target) && event.target !== menuNavToggle) {
        navMenu.classList.remove('show');
    }
});


let canClickMobileMenuNavToggle = true;
menuMobileNavToggle.addEventListener('click', function() {
    if (!canClickMobileMenuNavToggle) return;
    canClickMobileMenuNavToggle = false;
    mobileNavMenu.classList.toggle('open');

    setTimeout(function() {
        canClickMobileMenuNavToggle = true;
    }, 150);
});

document.addEventListener('click', function(event) {
    if (mobileNavMenu.classList.contains('open') && !event.target.closest('.nav')) {
        mobileNavMenu.classList.remove('open');
    }
})

navLinks.forEach(link => {
    link.addEventListener('click', function() {
        mobileNavMenu.classList.remove('open');
    })
})