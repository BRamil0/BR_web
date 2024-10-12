

// Завантажуємо тему з куків при завантаженні сторінки
window.onload = () => {
    const theme = getCookie('theme') || 'system';
    const savedLanguage = getCookie('language') || 'ukr'; // Встановити мову за замовчуванням
    applyTheme(theme);
    setLanguageMenu()
    loadLocalization(savedLanguage);
};