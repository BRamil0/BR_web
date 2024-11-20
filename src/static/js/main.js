const topButton = document.getElementById("top-button");
const bostonButton = document.getElementById("boston-button");
let theme = 'system';
let savedLanguage = 'eng';
let is_show_navigation_buttons = true;

document.addEventListener("DOMContentLoaded", async () => {
    theme = await getTheme();
    savedLanguage = await getLanguage();
    await updateBackground();
    await applyTheme(theme);
    await loadLocalization(savedLanguage);
    await setThemeMenu();
    await setLanguageMenu();
    await setAccountMenu();
});

window.onload = async () => {
    await updateModalButton();
    await updateMessageButton()
    await checkScroll();
    await updateCopyTextElements();
    await sendBrowserInfo();
    setTimeout(async () => {
        await hideLoadingBanner()
    }, 350);
};

window.onscroll = async function() {
    if (is_show_navigation_buttons) {
        await checkScroll();
    }
};

async function showInfoAlert(langKey) {
    const infoAlert = document.getElementById("info-alert");
    let newInfoAlert = infoAlert.cloneNode(true);

    newInfoAlert.id = "info-alert-" + Date.now();
    document.body.appendChild(newInfoAlert);

    let text = await getTextForKeyInLanguage(await getLanguage(), langKey);
    if (!text) {
        text = langKey;
    }

    newInfoAlert.textContent = text;
    newInfoAlert.classList.add('show');

    setTimeout(() => {
        newInfoAlert.classList.remove('show');
        setTimeout(() => {
            newInfoAlert.remove();
        }, 500);
    }, 3000);
}
async function checkScroll() {
    if (!is_show_navigation_buttons) {
        return;
    }
    const documentHeight = document.documentElement.scrollHeight;
    const windowHeight = window.innerHeight;
    if (documentHeight - 1 > windowHeight) {
        topButton.classList.add("show");
        bostonButton.classList.add("show");
    } else {
        topButton.classList.remove("show");
        bostonButton.classList.remove("show");
    }
}

topButton.addEventListener("click", async () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

bostonButton.addEventListener("click", async () => {
    window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: "smooth"
    });
});

// function isCheckingButton(className, event) {
//     for (let i = 0; i < className.length; i++) {
//         if (event.target === className[i]) {
//             return true;
//         }
//     }
//     return false;
// }

async function isCheckingButton(buttons, event) {
    return Array.from(buttons).some(button => button.contains(event.target));
}

async function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=None; Secure`;
}

let timeout1, timeout2, timeout3;
async function showLoadingBanner() {
    const loadingBanner = document.getElementById('loading-banner');
    const text1 = document.getElementById('loading-banner-text-1');
    const text2 = document.getElementById('loading-banner-text-2');
    const text3 = document.getElementById('loading-banner-text-3');
    loadingBanner.classList.remove('hidden');

    timeout1 = setTimeout(() => {
        text1.classList.add('show');
        timeout2 = setTimeout(() => {
            text1.classList.remove('show');
            text2.classList.add('show');
            timeout3 = setTimeout(() => {
                text2.classList.remove('show');
                text3.classList.add('show');
            }, 8000);
        }, 4000);
    }, 2000);
}

async function hideLoadingBanner() {
    const loadingBanner = document.getElementById('loading-banner');
    loadingBanner.classList.add('hidden');

    if (timeout1) clearTimeout(timeout1);
    if (timeout2) clearTimeout(timeout2);
    if (timeout3) clearTimeout(timeout3);
}

document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', async function() {
        this.classList.add('button-active');

        setTimeout(() => {
            this.classList.remove('button-active');
        }, 1000); //
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

        return await response.json();
    } catch (error) {
        console.error('Error sending browser info:', error);
        return false;
    }
};