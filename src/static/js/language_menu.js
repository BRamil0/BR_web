const languageButton = document.getElementById('language-button-menu');
const languageMenu = document.getElementById('language-menu');
const languageName = document.getElementById('language-name');
const languageEmoji = document.getElementById('language-emoji');

const languageList = ["eng", "ukr"]


function setLanguageMenu() {
    for (const lang of languageList) {
        fetch(`/static/localizations/${lang}_language.json`).then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
            .then(data => {
                languageMenu.innerHTML += `<button data-lang="${lang}" class="emoji-button">${data["info"]["emoji"]} ${data["info"]["original_name"]}</button>`;
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
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
            // Зберігаємо вибір користувача в куках
            setCookie('language', lang, 7);
            setLanguageName(data)


        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// Обробник для відкриття/закриття меню мов
languageButton.addEventListener('click', () => {
    languageMenu.classList.toggle('show'); // Тепер меню буде перемикатися при натисканні
});

// Закриття меню при натисканні поза ним
document.addEventListener('click', function(event) {
    if (!languageMenu.contains(event.target) && !languageButton.contains(event.target)) {
        languageMenu.classList.remove('show');
    }
});

// Обробник для вибору мови з меню
languageMenu.addEventListener('click', function(event) {
    const selectedLang = event.target.getAttribute('data-lang');
    if (selectedLang) {
        loadLocalization(selectedLang);
        languageMenu.classList.remove('show'); // Закриваємо меню після вибору мови
    }
});

// Функції для роботи з куками
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=None; Secure`;
}