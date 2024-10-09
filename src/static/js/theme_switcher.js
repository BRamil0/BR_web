const toggleButton = document.getElementById('theme-toggle');
const body = document.body;

// Функція для отримання значення куків
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Функція для встановлення куків
function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

// Завантажуємо тему з куків при завантаженні сторінки
window.onload = () => {
    const theme = getCookie('theme') || 'light';
    body.setAttribute('theme', theme);
};

// Обробник подій для перемикання теми
toggleButton.addEventListener('click', () => {
    const currentTheme = body.getAttribute('theme');

    // Перемикаємо тему
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    body.setAttribute('theme', newTheme);

    // Записуємо нову тему в куки
    setCookie('theme', newTheme, 7); // Кука зберігатиметься 7 днів
});