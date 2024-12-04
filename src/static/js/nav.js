import * as theme from "./theme.js";
import * as language from "./language.js";
import * as account from "./account.js";

const navMenu = document.getElementById('nav-menu');
const themeMenu = document.getElementById('theme-menu');
const languageMenu = document.getElementById('language-menu');
const accountMenu = document.getElementById("account-menu");

export async function updateNavButtons() {
    await updateMenuButtons('.nav-menu-button', navMenu);
    await updateMenuButtons('.theme-button-menu', themeMenu);
    await updateMenuButtons('.language-button-menu', languageMenu);
    await updateMenuButtons('.account-button-menu', accountMenu);
}

async function updateMenuButtons(selector, menuElement) {
    const buttons = document.querySelectorAll(selector);

    buttons.forEach(button => button.replaceWith(button.cloneNode(true)));

    document.querySelectorAll(selector).forEach(button => {
        button.addEventListener('click', async () => {
            await toggleMenu(menuElement);
        });
    });
}

async function toggleMenu(menuElement) {
    menuElement.classList.toggle('show');
}

async function updateMenu(menuElement, list, menuType) {
    menuElement.classList.remove("show");
    if (menuElement.innerHTML !== "") {
        await delMenu(menuElement);
        await new Promise(resolve => {setTimeout(() => {resolve();}, 100);});
    }

    try {
        let data = await language.getTextInLanguage(await language.getLanguage());
        for (const item of list) {
            if (menuType === "lang") {
                data = await language.getTextInLanguage(item);
                menuElement.innerHTML += `<button data-lang="${item}" class="emoji-button-menu jetbrains-mono-br">${data["info"]["emoji"]} ${data["info"]["original_name"]}</button>`;
            } else if (menuType === "theme") {
                menuElement.innerHTML += `<button data-translate="theme_${item}" data-theme="${item}" class="emoji-button-menu jetbrains-mono-br">${data["theme_" + item]}</button>`;
            }
        }
    } catch (error) {
        console.error(`There has been a problem with your fetch operation for ${menuType}:`, error);
        return false;
    }

    menuElement.addEventListener('click', async function (event) {
        const selectedItem = event.target.getAttribute(`data-${menuType}`);
        if (selectedItem) {
            if (menuType === "theme") {
                await theme.applyTheme(selectedItem);
            } else if (menuType === "lang") {
                await language.loadLocalization(selectedItem);
            }
            menuElement.classList.remove('show');
        }
    });

    return true;
}

export async function setThemeMenu() {
    const themeList = await setThemeList();
    await updateMenu(themeMenu, themeList, "theme");
}

export async function setLanguageMenu() {
    const languageList = await setLanguageList();
    await updateMenu(languageMenu, languageList, "lang");
}

export async function setAccountMenu() {
    accountMenu.classList.remove("show");
    if (accountMenu.innerHTML !== "") {
        await delMenu(accountMenu);
        await new Promise(resolve => {setTimeout(() => {resolve();}, 100);});
    }

    try {
        let dataLanguage = await language.getTextInLanguage(await language.getLanguage());
            if (!dataLanguage) {
                console.error('dataLanguage is undefined or empty.');
                return false;
            }
        if (await account.isAuthenticated()) {
            accountMenu.innerHTML += `<a href="/account/profile/my" data-account="profile" data-translate="account_profile_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_profile_button"] || "Профіль"}</a>`;
            accountMenu.innerHTML += `<a href="/account/settings" data-account="settings" data-translate="account_settings_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_settings_button"] || "Налаштування"}</a>`;
            accountMenu.innerHTML += `<button id="form-logout-button" data-account="logout" data-translate="account_logout_button" class="jetbrains-mono-br">${dataLanguage["account_logout_button"] || "Вихід"}</button>`;
        } else {
            accountMenu.innerHTML += `<a href="/account/login" data-account="login" data-translate="account_login_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_login_button"] || "Авторизація"}</a>`;
            accountMenu.innerHTML += `<a href="/account/register" data-account="register" data-translate="account_register_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_register_button"] || "Реєстрація"}</a>`;
        }
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return false;
    }

    accountMenu.addEventListener('click', async function (event) {
        const selectedItem = event.target.getAttribute(`data-account`);
        if (selectedItem) {
            if (selectedItem === "logout") {
                await account.logoutAccount();
            }
            accountMenu.classList.remove('show');
        }
    })

    return true;
}

export async function delMenu(menuElement) {
    if (menuElement && menuElement instanceof HTMLElement) {
        menuElement.innerHTML = "";
    } else {
        console.error(`${menuElement} is not a valid DOM element`);
    }
}

async function setThemeList() {
    try {
        const response = await fetch('/api/theme_list');
        if (!response.ok) {
            console.error(`Failed to load language file for "theme_list"`);
            return ["light", "dark", "system"];
        }
        const data = await response.json();
        return data['theme_list'];
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return ["light", "dark", "system"];
    }
}

async function setLanguageList() {
    try {
        const response = await fetch('/api/language_list');
        if (!response.ok) {
            console.error(`Failed to load language file for "language_list"`);
            return ["ukr", "eng"];
        }
        const data = await response.json();
        return data['language_list'];
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return ["ukr", "eng"];
    }
}

document.addEventListener('click', function (event) {
    if (!event.target.closest('.nav-menu-button') && !navMenu.contains(event.target)) {
        navMenu.classList.remove('show');
    }
    if (!event.target.closest('.theme-button-menu') && !themeMenu.contains(event.target)) {
        themeMenu.classList.remove('show');
    }
    if (!event.target.closest('.language-button-menu') && !languageMenu.contains(event.target)) {
        languageMenu.classList.remove('show');
    }
    if (!event.target.closest('.account-button-menu') && !accountMenu.contains(event.target)) {
        accountMenu.classList.remove("show");
    }
});