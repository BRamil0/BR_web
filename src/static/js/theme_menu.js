const themeButtonMenu = document.getElementById('theme-button-menu');
const themeMenu = document.getElementById('theme-menu');
const themeEmoji = document.getElementById('theme-emoji');
const body = document.body;

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

async function setThemeMenu() {
    const themeList = await setThemeList();
    const Language = await getCookie('language') || savedLanguage;
    try {
        const response = await fetch(`/static/localizations/${Language}_language.json`);
        if (!response.ok) {
            console.error(`Failed to load language file for ${Language}`);
            return false;
        }
        const data = await response.json();
        themeList.forEach(theme => {
            themeMenu.innerHTML += `<button data-translate="theme_${theme}" data-theme="${theme}" class="emoji-button-menu jetbrains-mono-br">${data["theme_" + theme]}</button>`;
        });
        return true;
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return false;
    }
}

async function delThemeMenu() {
    const themeList = await setThemeList(); // Wait for theme list
    themeList.forEach(theme => {
        document.querySelectorAll(`[data-theme="${theme}"]`).forEach(element => {
            element.remove();
        });
    });
}

async function setThemeEmoji(value) {
    if (value === "light") themeEmoji.textContent = "☀️";
    else if (value === "dark") themeEmoji.textContent = "🌒";
    else themeEmoji.textContent = "🔃";
}

async function applyTheme(theme) {
    let system = false;
    await setCookie('theme', theme, 7);
    if (theme === 'system') {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = systemPrefersDark ? 'dark' : 'light';
        system = true;
    }
    body.setAttribute('theme', theme);
    if (!system) {
        await setThemeEmoji(theme);
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

document.addEventListener('click', async function(event) {
    if (!themeMenu.contains(event.target) && !themeButtonMenu.contains(event.target)) {
        themeMenu.classList.remove('show');
    }
});

themeMenu.addEventListener('click', async function(event) {
    const theme = event.target.getAttribute('data-theme');
    if (theme) {
        await applyTheme(theme);
        themeMenu.classList.remove('show');
    }
});