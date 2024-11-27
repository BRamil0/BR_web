import * as cookies from "./cookies.js";

export async function getLanguage() {
    try {
        const response = await fetch(`/api/default_language`);
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
        const response = await fetch(`/static/localizations/${lang}_language.json`);
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
        const response = await fetch(`/static/localizations/${lang}_language.json`);
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
                else if (element.tagName === 'BUTTON' || element.tagName === 'INPUT' && element.type === 'button') {
                    element.setAttribute('value', data[key]);
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

        await setLanguageName(data);
        document.documentElement.setAttribute('lang', lang);

        await cookies.setCookie('language', lang, 7);
        return true;
    } catch (error) {
        console.error('Localization loading failed:', error);
        return false;
    }
}

async function setLanguageName(lang) {
    languageName.textContent = lang["info"]["original_name"];
    languageEmoji.textContent = lang["info"]["emoji"];
}