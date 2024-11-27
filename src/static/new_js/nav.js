import * as theme from "./theme.js";
import * as language from "./language.js";

const navMenu = document.getElementById('nav-menu');
const themeMenu = document.getElementById('theme-menu');
const languageMenu = document.getElementById('language-menu');

export async function updateNavButtons() {
    await updateMenuButtons('.nav-menu-button', navMenu);
    await updateMenuButtons('.emoji-button-menu', themeMenu);
    await updateMenuButtons('.emoji-button-menu', languageMenu);
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
    }

    try {
        const data = await language.getTextInLanguage(await language.getLanguage());
        list.forEach(item => {
            if (menuType === "lang") {
                menuElement.innerHTML += `<button data-lang="${item}" class="emoji-button-menu jetbrains-mono-br">${data["info"]["emoji"]} ${data["info"]["original_name"]}</button>`;
            } else if (menuType === "theme") {
                menuElement.innerHTML += `<button data-translate="theme_${item}" data-theme="${item}" class="emoji-button-menu jetbrains-mono-br">${data["theme_" + item]}</button>`;
            }
        });
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

export async function delMenu(menuElement) {
    menuElement.innerHTML = "";
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
    if (!event.target.closest('.emoji-button-menu') && !themeMenu.contains(event.target)) {
        themeMenu.classList.remove('show');
    }
    if (!event.target.closest('.emoji-button-menu') && !languageMenu.contains(event.target)) {
        languageMenu.classList.remove('show');
    }
});