const theme = getCookie('theme') || 'system';
const savedLanguage = getCookie('language') || 'eng'; // Встановити мову за замовчуванням

document.addEventListener("DOMContentLoaded", async () => {
    await updateBackground();
    await applyTheme(theme);
    await loadLocalization(savedLanguage);
    await sendBrowserInfo();
    await setThemeMenu();
    await setLanguageMenu();
    console.log("DOM fully loaded and parsed");
});

window.onload = async () => {
    setTimeout(() => {
        hideLoadingBanner()
    }, 350);
    console.log("Page loaded");
};

function isCheckingButton(className, event) {
    for (let i = 0; i < className.length; i++) {
        if (event.target === className[i]) {
            return true;
        }
    }
    return false;
}


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

document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function() {
        // Додаємо клас активного стану
        this.classList.add('button-active');

        // Знімаємо клас через 1 секунду
        setTimeout(() => {
            this.classList.remove('button-active');
        }, 1000); // 1000 мілісекунд = 1 секунда
    });
});

async function sendBrowserInfo() {
    const data = {
        innerWidth: window.innerWidth.toString(),
        innerHeight: window.innerHeight.toString(),
        screen_width: screen.width.toString(),
        screen_height: screen.height.toString(),
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        location_href: window.location.href,
        connection_downlink: navigator.connection ? navigator.connection.downlink.toString() : 'unknown',
        connection_effective_type: navigator.connection ? navigator.connection.effectiveType : 'unknown',
        online: navigator.onLine.toString(),
        performance_timing: JSON.stringify(performance.timing),

        // Додаткові дані
        max_touch_points: navigator.maxTouchPoints.toString(),
        hardware_concurrency: navigator.hardwareConcurrency.toString(),
        device_memory: navigator.deviceMemory ? navigator.deviceMemory.toString() : 'unknown',
        color_depth: screen.colorDepth.toString(),
        pixel_depth: screen.pixelDepth.toString(),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        cookies_enabled: navigator.cookieEnabled.toString(),
        referrer: document.referrer || 'no-referrer',
        visibility_state: document.visibilityState,
        document_title: document.title,
        page_load_time: (performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart).toString()
    };

    try {
        const response = await fetch('/api/telegram/info/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log('Server response:', result);
    } catch (error) {
        console.error('Error sending browser info:', error);
    }
};