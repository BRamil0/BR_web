const languageButton = document.getElementById('language-button-menu');
const languageMenu = document.getElementById('language-menu');
const languageName = document.getElementById('language-name');
const languageEmoji = document.getElementById('language-emoji');

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

async function setLanguageMenu() {
    const languageList = await setLanguageList();

    for (const lang of languageList) {
        try {
            const response = await fetch(`/static/localizations/${lang}_language.json`);
            if (!response.ok) {
                console.error(`Failed to load language file for ${lang}`);
                return false;
            }
            const data = await response.json();
            languageMenu.innerHTML += `<button data-lang="${lang}" class="emoji-button-menu jetbrains-mono-br">${data["info"]["emoji"]} ${data["info"]["original_name"]}</button>`;
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
            return false;
        }
    }
}

async function delLanguageMenu() {
    const languageList = await setLanguageList();
    languageList.forEach(lang => {
        document.querySelectorAll(`[data-lang="${lang}"]`).forEach(element => {
            element.remove();
        });
    });
}

async function setLanguageName(lang) {
    languageName.textContent = lang["info"]["original_name"];
    languageEmoji.textContent = lang["info"]["emoji"];
}

async function getTextForKeyInLanguage(lang, key) {
    const text = await getTextInLanguage(lang);
    if (!text || !text[key]) {
        return key;
    }
    return text[key];
}

async function getTextInLanguage(lang) {
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

async function loadLocalization(lang) {
    try {
        const response = await fetch(`/static/localizations/${lang}_language.json`);
        if (!response.ok) {
            return false;
        }
        const data = await response.json();

        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (data[key]) {
                const placeholder = "placeholder_";
                if (key.includes(placeholder)) {
                    element.setAttribute('placeholder', data[key]);
                } else {
                    element.textContent = data[key];
                }
            }
        });

        await setCookie('language', lang, 7);
        await setLanguageName(data);
        document.getElementsByTagName('html')[0].setAttribute('lang', lang);
        return true;
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return false;
    }
}

languageButton.addEventListener('click', function() {
    if (languageMenu.classList.contains('show')) {
        languageMenu.classList.remove('show');
    } else {
        languageMenu.classList.add('show');
    }
});

document.addEventListener('click', function(event) {
    if (!languageMenu.contains(event.target) && !languageButton.contains(event.target)) {
        languageMenu.classList.remove('show');
    }
});

languageMenu.addEventListener('click',  async function(event) {
    const selectedLang = event.target.getAttribute('data-lang');
    if (selectedLang) {
        await loadLocalization(selectedLang);
        languageMenu.classList.remove('show');
    }
});
