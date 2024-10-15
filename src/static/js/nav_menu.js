const navMenu =  document.querySelector('.nav')
const menuNavToggle = document.getElementById('menu-toggle')
const navLinks = navMenu.querySelectorAll('.nav-link') // Select all nav link


let canClickMenuNavToggle = true;
menuNavToggle.addEventListener('click', function() {
    if (!canClickButtonMenu) return;
    canClickMenuNavToggle = false;
    navMenu.classList.toggle('open');

    setTimeout(function() {
        canClickMenuNavToggle = true;
    }, 300);
});

document.addEventListener('click', function(event) {
    if (navMenu.classList.contains('open') && !event.target.closest('.nav')) {
        navMenu.classList.remove('open');
    }
})

navLinks.forEach(link => {
    link.addEventListener('click', function() {
        navMenu.classList.remove('open');
    })
})