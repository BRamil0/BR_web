// Список мов (додайте свої мови тут)
const languages = [
    { code: 'ukr', name: 'Українська', emoji: '🇺🇦' },
    { code: 'en', name: 'English', emoji: '🇬🇧' },
    // Додайте інші мови за потреби
];

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

// Функція для ініціалізації меню мов
function initLanguageMenu() {
    const languageMenu = document.getElementById('language-menu');
    languages.forEach(lang => {
        const button = document.createElement('button');
        button.textContent = `${lang.emoji} ${lang.name}`;
        button.dataset.lang = lang.code;
        button.addEventListener('click', () => {
            switchLanguage(lang.code);
            toggleLanguageMenu(); // закриваємо меню після вибору
        });
        languageMenu.appendChild(button);
    });
}

// Функція для перемикання мови
function switchLanguage(language) {
    setCookie('language_code', language, 7); // Зберігайте мову на 7 днів
    loadLanguage(language);
}

// Функція для показу/сховання меню
function toggleLanguageMenu() {
    const languageMenu = document.getElementById('language-menu');
    languageMenu.style.display = languageMenu.style.display === 'block' ? 'none' : 'block';
}

// Вибір мови при завантаженні сторінки
window.onload = () => {
    const language = getCookie('language_code') || 'ukr'; // За замовчуванням українська
    loadLanguage(language);
    initLanguageMenu(); // Ініціалізація меню мов
};

// Додавання обробника для кнопки перемикання меню
document.getElementById('language-toggle').addEventListener('click', toggleLanguageMenu);

// Додавання обробника для натискань поза меню
window.addEventListener('click', (event) => {
    const languageMenu = document.getElementById('language-menu');
    if (!event.target.matches('#language-toggle') && !languageMenu.contains(event.target)) {
        languageMenu.style.display = 'none'; // Закриваємо меню
    }
});