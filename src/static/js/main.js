const languageList = ["eng", "ukr"]
const themeList = ["light", "dark", "system"];
const theme = getCookie('theme') || 'system';
const savedLanguage = getCookie('language') || 'ukr'; // Встановити мову за замовчуванням

document.addEventListener("DOMContentLoaded", async () => {
    await updateBackground();
    await applyTheme(theme);
    await loadLocalization(savedLanguage);
    console.log("DOM fully loaded and parsed");
});

window.onload = async () => {
    setTimeout(() => {
        hideLoadingBanner()
    }, 350);
    console.log("Page loaded");
};

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

// Показуємо банер при завантаженні сторінки
function showLoadingBanner() {
    const loadingBanner = document.getElementById('loading-banner');
    loadingBanner.classList.remove('hidden'); // Робимо банер видимим
}

// Приховуємо банер після завершення завантаження
function hideLoadingBanner() {
    const loadingBanner = document.getElementById('loading-banner');
    loadingBanner.classList.add('hidden'); // Прибираємо банер після завантаження
}