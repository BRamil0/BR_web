const mobileNavMenu = document.querySelector('.nav-center')
const menuMobileNavToggle = document.getElementById('mobile-menu-toggle')
const navLinks = mobileNavMenu.querySelectorAll('.mobile-nav-link') // Select all nav link
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