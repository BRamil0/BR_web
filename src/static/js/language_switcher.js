// Функція для отримання куки
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Функція для встановлення куки
function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/;SameSite=None;Secure`;
}

// Функція для завантаження мови
async function loadLanguage(language) {
    try {
        const response = await fetch(`/static/localizations/${language}_language.json`);
        if (!response.ok) throw new Error('Network response was not ok');
        const translations = await response.json();

        // Оновлення тексту на сторінці
        for (const [key, value] of Object.entries(translations)) {
            const elements = document.querySelectorAll(`[data-translate="${key}"]`);
            elements.forEach((element) => {
                element.textContent = value;
            });
        }
    } catch (error) {
        console.error('Error loading language:', error);
    }
}

// Функція для перемикання мови
function switchLanguage(language) {
    setCookie('language_code', language, 7); // Зберігайте мову на 7 днів
    loadLanguage(language);
}

// Вибір мови при завантаженні сторінки
window.onload = () => {
    const language = getCookie('language_code') || 'ukr'; // За замовчуванням українська
    loadLanguage(language);
};

// Додавання обробника для кнопок перемикання
document.addEventListener('DOMContentLoaded', () => {
    const languageButtons = document.querySelectorAll('.language-switcher');
    languageButtons.forEach(button => {
        button.addEventListener('click', () => {
            switchLanguage(button.dataset.lang);
        });
    });
});
