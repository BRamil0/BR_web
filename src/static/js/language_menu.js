const languageButton = document.getElementById('language-button-menu');
const languageMenu = document.getElementById('language-menu');
const languageName = document.getElementById('language-name');
const languageEmoji = document.getElementById('language-emoji');

function setLanguageMenu() {
    for (const lang of languageList) {
        fetch(`/static/localizations/${lang}_language.json`).then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
            .then(data => {
                languageMenu.innerHTML += `<button data-lang="${lang}" class="emoji-button jetbrains-mono-br">${data["info"]["emoji"]} ${data["info"]["original_name"]}</button>`;
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


// Функція для завантаження файлу локалізації
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
                    element.textContent = data[key];
                }
            });
            setCookie('language', lang, 7);
            setLanguageName(data)


        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// Обробник для відкриття/закриття меню мов
languageButton.addEventListener('click', () => {
    if (languageMenu.classList.contains('show')) {
        languageMenu.classList.remove('show');
        setTimeout(() => {
            delLanguageMenu();
        }, 300);
    } else {
        setLanguageMenu();
        setTimeout(() => {
            languageMenu.classList.add('show');
        }, 100);
    }
});

// Закриття меню при натисканні поза ним
document.addEventListener('click', function(event) {
    if (!languageMenu.contains(event.target) && !languageButton.contains(event.target)) {
        languageMenu.classList.remove('show');
        setTimeout(() => {
            delLanguageMenu();
        }, 300);
    }
});

// Обробник для вибору мови з меню
languageMenu.addEventListener('click', function(event) {
    const selectedLang = event.target.getAttribute('data-lang');
    if (selectedLang) {
        loadLocalization(selectedLang);
        languageMenu.classList.remove('show'); // Закриваємо меню після вибору мови
        setTimeout(() => {
            delLanguageMenu();
        }, 300);
    }
});