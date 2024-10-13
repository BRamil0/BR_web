const toggleButtonMenu = document.getElementById('theme-button-menu');
const themeEmoji = document.getElementById('theme-emoji');
const body = document.body;

const themeMenu = document.getElementById('theme-menu');

function setThemeMenu() {
    for (let theme of themeList) {
        themeMenu.innerHTML += `<button data-translate="theme_${theme}" data-theme ="${theme}" class="emoji-button jetbrains-mono-br">${themeList[theme]}</button>`
    }
    const savedLanguage = getCookie('language') || 'ukr'; // Встановити мову за замовчуванням
    loadLocalization(savedLanguage);
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
        // Застосовуємо системну тему
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

themeMenu.addEventListener('click', function(event) {
    const theme = event.target.getAttribute('data-theme');
    if (theme) {
        applyTheme(theme);
        themeMenu.classList.remove('show');
        setTimeout(() => {
            delThemeMenu();
        }, 300);
    }
});

// Показуємо меню тем
toggleButtonMenu.addEventListener('click', () => {
    if (themeMenu.classList.contains('show')) {
        themeMenu.classList.remove('show');
        setTimeout(() => {
            delThemeMenu();
        }, 300);
    } else {
        setThemeMenu();
        setTimeout(() => {
            themeMenu.classList.add('show');
        }, 10);
    }
});

// Закриття меню при натисканні поза ним
document.addEventListener('click', function(event) {
    const themeMenu = document.getElementById('theme-menu');
    if (!themeMenu.contains(event.target) && !toggleButtonMenu.contains(event.target)) {
        themeMenu.classList.remove('show');
        setTimeout(() => {
            delThemeMenu();
        }, 300);
    }
});
