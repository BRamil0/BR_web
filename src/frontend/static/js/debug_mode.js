import * as nav from "./nav.js";
import * as loading_banner from "./loading_banner.js";
import * as info_alert from "./info_alert.js";

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

    async function clearCookies() {
        const domain = window.location.hostname;
        const paths = ['/'];

        document.cookie.split(';').forEach(cookie => {
            const cookieName = cookie.trim().split('=')[0];

            if (cookieName) {
                paths.forEach(path => {
                    document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path}; domain=${domain}; SameSite=None; Secure`;
                });
            }
        });
        console.log("Cookies очищено!");
        await info_alert.showInfoAlert("cookies_cleared");
    }

    async function clearCache() {
        if ('caches' in window) {
            caches.keys().then(function(names) {
                names.forEach(function(name) {
                    caches.delete(name);
                });
            });
        }
        console.log("Кеш очищено!");
        await info_alert.showInfoAlert("cache_cleared");
    }

    async function reloadPage() {
        window.location.reload();
    }

    async function delThemeMenu() {
        await nav.delMenu(document.getElementById("theme-menu"));
        console.log("Меню тем очищено!");
        await info_alert.showInfoAlert("theme_menu_cleared");
    }

    async function delLanguageMenu() {
        await nav.delMenu(document.getElementById("language-menu"));
        console.log("Меню мов очищено!");
        await info_alert.showInfoAlert("language_menu_cleared");
    }

    async function delAccountMenu() {
        await nav.delMenu(document.getElementById("account-menu"));
        console.log("Меню облікового запису очищено!");
        await info_alert.showInfoAlert("account_menu_cleared");
    }

    document.getElementById("reload-page-button").addEventListener("click", reloadPage);
    document.getElementById("clear-cookies-button").addEventListener("click", clearCookies);
    document.getElementById("clear-cache-button").addEventListener("click", clearCache);
    document.getElementById("clear-theme-button").addEventListener("click", delThemeMenu);
    document.getElementById("clear-language-button").addEventListener("click", delLanguageMenu);
    document.getElementById("clear-account-button").addEventListener("click", delAccountMenu);
    document.getElementById("on-banner-button").addEventListener("click", loading_banner.showLoadingBanner);
    document.getElementById("off-banner-button").addEventListener("click", loading_banner.hideLoadingBanner);
});