const toggleButtonMenu = document.getElementById('theme-button-menu');
const themeEmoji = document.getElementById('theme-emoji');
const body = document.body;

const themeMenu = document.getElementById('theme-menu');

function setThemeMenu() {
    const savedLanguage = getCookie('language') || 'ukr';
    fetch(`/static/localizations/${savedLanguage}_language.json`).then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
                for (let theme of themeList) {
                    themeMenu.innerHTML += `<button data-translate="theme_${theme}" data-theme ="${theme}" class="emoji-button jetbrains-mono-br">${data["theme_" + theme]}</button>`
                }
            })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}


function delThemeMenu() {
    for (let theme of themeList) {
        document.querySelectorAll(`[data-theme="${theme}"]`).forEach(element => {element.remove();
        })
    }
}

// Функція для встановлення емодзі теми
function setThemeEmoji(value) {
    if (value === "light") themeEmoji.textContent = "☀️";
    else if (value === "dark") themeEmoji.textContent = "🌒";
    else themeEmoji.textContent = "🔃";
}

// Функція для встановлення теми
function applyTheme(theme) {
    let system = false;
    setCookie('theme', theme, 7);
    if (theme === 'system') {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = systemPrefersDark ? 'dark' : 'light';
        system = true
    }
    body.setAttribute('theme', theme);
    if (system === false) {
        setThemeEmoji(theme);
    } else {
        themeEmoji.textContent = "🖥️";
    }
}

let canClickThemeMenu = true;
themeMenu.addEventListener('click', function(event) {
    if (!canClickThemeMenu) return;
    canClickThemeMenu = false;
    const theme = event.target.getAttribute('data-theme');
    if (theme) {
        applyTheme(theme);
        themeMenu.classList.remove('show');
    }
    setTimeout(() => {
        canClickThemeMenu = true;
    }, 200);
});

let canClickThemeButtonMenu = true;
toggleButtonMenu.addEventListener('click', () => {
    if (!canClickThemeButtonMenu) return;
    canClickThemeButtonMenu = false;

    if (themeMenu.classList.contains('show')) {
        themeMenu.classList.remove('show');
    } else {
        themeMenu.classList.add('show');
    }

    setTimeout(() => {
        canClickThemeButtonMenu = true;
    }, 150);
});

document.addEventListener('click', function(event) {
    const themeMenu = document.getElementById('theme-menu');
    if (!themeMenu.contains(event.target) && !toggleButtonMenu.contains(event.target)) {
        themeMenu.classList.remove('show');
    }
});
