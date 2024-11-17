document.addEventListener("DOMContentLoaded", function() {
    const debugModeButton = document.getElementById("debug-mode-menu-button");
    const debugModeMenu = document.getElementById("debug-mode-menu");

    debugModeButton.addEventListener("click", () => {
        if (debugModeMenu.classList.contains("show")) {
            debugModeMenu.classList.remove("show");
        } else {
            debugModeMenu.classList.add("show");
        }
    });

    document.addEventListener("click", (event) => {
        if (!debugModeMenu.contains(event.target) && !debugModeButton.contains(event.target)) {
            debugModeMenu.classList.remove("show");
        }
    });

    function clearCookies() {
        document.cookie.split(';').forEach(function(c) {
            document.cookie = c.trim().split('=')[0] + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
        });
        alert("Cookies очищено!");
    }

    function clearCache() {
        if ('caches' in window) {
            caches.keys().then(function(names) {
                names.forEach(function(name) {
                    caches.delete(name);
                });
            });
        }
        alert("Кеш очищено!");
    }

    function reloadPage() {
        window.location.reload();
    }

    document.getElementById("reload-page-button").addEventListener("click", reloadPage);
    document.getElementById("clear-cookies-button").addEventListener("click", clearCookies);
    document.getElementById("clear-cache-button").addEventListener("click", clearCache);
    document.getElementById("clear-theme-button").addEventListener("click", delThemeMenu);
    document.getElementById("clear-language-button").addEventListener("click", delLanguageMenu);
    document.getElementById("clear-account-button").addEventListener("click", delAccountMenu);
});