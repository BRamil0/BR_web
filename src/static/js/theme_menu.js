const themeButtonMenu = document.getElementById('theme-button-menu');
const themeMenu = document.getElementById('theme-menu');
const themeEmoji = document.getElementById('theme-emoji');
const body = document.body;
const themeList = setThemeList()

function setThemeList() {
    fetch('/api/theme_list').then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
        .then(data => {
            return data['theme_list'];
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    return ["light", "dark", "system"];
}

function setThemeMenu() {
    const savedLanguage = getCookie('language') || 'ukr';
    fetch(`/static/localizations/${savedLanguage}_language.json`).then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
                for (let theme of themeList) {
                    themeMenu.innerHTML += `<button data-translate="theme_${theme}" data-theme ="${theme}" class="emoji-button-menu jetbrains-mono-br">${data["theme_" + theme]}</button>`
                }
            })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

function delThemeMenu() {
    for (let theme of themeList) {
        document.querySelectorAll(`[data-theme="${theme}"]`).forEach(element => {element.remove();
        })
    }
}

function setThemeEmoji(value) {
    if (value === "light") themeEmoji.textContent = "☀️";
    else if (value === "dark") themeEmoji.textContent = "🌒";
    else themeEmoji.textContent = "🔃";
}

function applyTheme(theme) {
    let system = false;
    setCookie('theme', theme, 7);
    if (theme === 'system') {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = systemPrefersDark ? 'dark' : 'light';
        system = true
    }
    body.setAttribute('theme', theme);
    if (system === false) {
        setThemeEmoji(theme);
    } else {
        themeEmoji.textContent = "🖥️";
    }
}

themeButtonMenu.addEventListener('click', () => {
    if (themeMenu.classList.contains('show')) {
        themeMenu.classList.remove('show');
    } else {
        themeMenu.classList.add('show');
    }
});

document.addEventListener('click', function(event) {
    const themeMenu = document.getElementById('theme-menu');
    if (!themeMenu.contains(event.target) && !themeButtonMenu.contains(event.target)) {
        themeMenu.classList.remove('show');
    }
});

themeMenu.addEventListener('click', function(event) {
    const theme = event.target.getAttribute('data-theme');
    if (theme) {
        applyTheme(theme);
        themeMenu.classList.remove('show');
    }
});