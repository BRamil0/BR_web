const toggleButtonMenu = document.getElementById('theme-button-menu');
const themeEmoji = document.getElementById('theme-emoji');
const body = document.body;

const lightThemeButton = document.getElementById('light-theme');
const darkThemeButton = document.getElementById('dark-theme');
const systemThemeButton = document.getElementById('system-theme');

// Функція для отримання значення куків
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Функція для встановлення куків
function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=None; Secure`;
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

// Обробник подій для кожної кнопки теми
lightThemeButton.addEventListener('click', () => {
    applyTheme('light');
    setCookie('theme', 'light', 7);
});

darkThemeButton.addEventListener('click', () => {
    applyTheme('dark');
    setCookie('theme', 'dark', 7);
});

systemThemeButton.addEventListener('click', () => {
    applyTheme('system');
    setCookie('theme', 'system', 7);
});

// Показуємо меню тем
toggleButtonMenu.addEventListener('click', () => {
    document.getElementById('theme-menu').classList.add('show');
});

// Закриття меню при натисканні поза ним
document.addEventListener('click', function(event) {
    const themeMenu = document.getElementById('theme-menu');
    if (!themeMenu.contains(event.target) && !toggleButtonMenu.contains(event.target)) {
        themeMenu.classList.remove('show');
    }
});
