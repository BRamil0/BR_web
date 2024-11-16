const languageButton = document.getElementById('language-button-menu');
const languageMenu = document.getElementById('language-menu');
const languageName = document.getElementById('language-name');
const languageEmoji = document.getElementById('language-emoji');
const languageList = setLanguageList();

function setLanguageList() {
    fetch('/api/language_list').then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
        .then(data => {
            return data['language_list'];
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    return ["eng", "ukr"];
}

function setLanguageMenu() {
    for (const lang of languageList) {
        fetch(`/static/localizations/${lang}_language.json`).then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
            .then(data => {
                languageMenu.innerHTML += `<button data-lang="${lang}" class="emoji-button-menu jetbrains-mono-br">${data["info"]["emoji"]} ${data["info"]["original_name"]}</button>`;
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    }
}

function delLanguageMenu() {
    for (const lang of languageList) {
        document.querySelectorAll(`[data-lang="${lang}"]`).forEach(element => {
            element.remove();
        })
    }
}

function setLanguageName(lang) {
    languageName.textContent = lang["info"]["original_name"];
    languageEmoji.textContent = lang["info"]["emoji"];
}


function loadLocalization(lang) {
    fetch(`/static/localizations/${lang}_language.json`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            document.querySelectorAll('[data-translate]').forEach(element => {
                const key = element.getAttribute('data-translate');
                if (data[key]) {
                    const placeholder = "placeholder_"
                    if (key.includes(placeholder)) {
                        element.setAttribute('placeholder', data[key]);
                    }
                    else
                        element.textContent = data[key];
                }
            });
            setCookie('language', lang, 7);
            setLanguageName(data)
            document.getElementsByTagName('html')[0].setAttribute('lang', lang);


        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
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

languageMenu.addEventListener('click', function(event) {
    const selectedLang = event.target.getAttribute('data-lang');
    if (selectedLang) {
        loadLocalization(selectedLang);
        languageMenu.classList.remove('show');
    }
});