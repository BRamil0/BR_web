const languageButton = document.getElementById('language-button-menu');
const languageMenu = document.getElementById('language-menu');
const languageName = document.getElementById('language-name');
const languageEmoji = document.getElementById('language-emoji');
let is_show_language_menu = true;

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
    is_show_language_menu = false;
    languageMenu.classList.remove("show");

    const languageList = await setLanguageList();

    setTimeout( async () => {
        if (languageMenu.innerHTML !== "") {
            await delLanguageMenu()
        }
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
        is_show_language_menu = true;
    }, 100);

    return true;
}

async function delLanguageMenu() {
    languageMenu.innerHTML = "";
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

async function getLanguage() {
    try {
        const response = await fetch(`/api/default_language`);
        if (!response.ok) {
            console.error(`Error fetching default language`);
            return "ukr";
        }
        let lang = await response.json();
        return await getCookie('language') || lang["language_default"] || "ukr";
    } catch (error) {
        console.error('Error fetching default language:', error);
        return "ukr";
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
    if (is_show_language_menu) {
        if (languageMenu.classList.contains('show')) {
            languageMenu.classList.remove('show');
        } else {
            languageMenu.classList.add('show');
        }
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
