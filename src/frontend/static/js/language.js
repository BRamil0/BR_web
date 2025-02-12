import * as cookies from "./cookies.js";
import {getURL} from "./tools.js";

export let isLoaded = false;

export async function getLanguage() {
    try {
        const response = await fetch(await getURL(`/api/default_language`));
        if (!response.ok) {
            console.error(`Error fetching default language`);
            return "ukr";
        }
        let lang = await response.json();
        return await cookies.getCookie('language') || lang["language_default"] || "ukr";
    } catch (error) {
        console.error('Error fetching default language:', error);
        return "ukr";
    }
}

export async function getTextForKeyInLanguage(lang, key) {
    const text = await getTextInLanguage(lang);
    if (!text || !text[key]) {
        return key;
    }
    return text[key];
}

export async function getTextInLanguage(lang) {
    try {
        const response = await fetch(await getURL(`/static/localizations/${lang}_language.json`));
        if (!response.ok) {
            console.error(`Failed to load language file for ${lang}`);
            return false;
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return false;
    }
}

export async function loadLocalization(lang) {
    try {
        const response = await fetch(await getURL(`/static/localizations/${lang}_language.json`));
        if (!response.ok) {
            console.error(`Localization file for "${lang}" not found.`);
            return false;
        }
        const data = await response.json();

        document.querySelectorAll('[data-translate], [data-translate-html]').forEach(element => {
            const key = element.getAttribute('data-translate') || element.getAttribute('data-translate-html');
            if (data[key]) {
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    element.setAttribute('placeholder', data[key]);
                }
                else if (element.tagName === 'META') {
                    if ("og:title" === element.hasAttribute('property')) {
                        element.setAttribute('content', data[key] + " | BR Web");
                    }
                    element.setAttribute('content', data[key]);
                }
                else if (element.tagName === 'TITLE') {
                    element.textContent = data[key] + " | BR Web";
                }
                else {
                    const isHTML = element.hasAttribute('data-translate-html');
                    if (isHTML) {
                        element.innerHTML = data[key];
                    } else {
                        element.textContent = data[key];
                    }
                }
            }
        });
        const languageName = document.querySelectorAll('.language-name');
        const languageEmoji = document.querySelectorAll('.language-emoji');

        for (const element of languageName) {
            if (element) await setLanguageName(data, element);
        }

        for (const element of languageEmoji) {
            if (element) await setLanguageEmoji(data, element);
        }

        document.documentElement.setAttribute('data-lang', data["info"]["code_3"]);
        document.documentElement.setAttribute('lang', data["info"]["code_2"]);

        await cookies.setCookie('language', data["info"]["code_3"], 7);
        isLoaded = true;

        return true;
    } catch (error) {
        console.error('Localization loading failed:', error);
        return false;
    }
}

async function setLanguageName(lang, languageName) {
    if (!languageName) {
        return;
    }
    languageName.textContent = lang["info"]["original_name"];
}

async function setLanguageEmoji(lang, languageEmoji) {
    if (!languageEmoji) {
        return;
    }
    languageEmoji.textContent = lang["info"]["emoji"];
}
