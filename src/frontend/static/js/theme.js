import * as cookies from "./cookies.js";
import {getURL} from "./tools.js";

export let isLoaded = false;

export async function getTheme() {
    try {
        const response = await fetch(await getURL(`/api/default_theme`));
        if (!response.ok) {
            console.error("Error fetching default theme");
            return "system";
        }
        let theme = await response.json();
        return await cookies.getCookie('theme') || theme["theme_default"] || "system";
    } catch (error) {
        console.error('Error fetching default theme:', error);
        return "system";
    }
}

export async function applyTheme(theme) {
    let system = false;
    let themeEmoji = document.getElementsByClassName('theme-emoji')
    await cookies.setCookie('theme', theme, 7);
    if (theme === 'system') {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = systemPrefersDark ? 'dark' : 'light';
        system = true;
    }
    document.body.setAttribute('theme', theme);
    if (!system) {
        for (let i = 0; i < themeEmoji.length; i++) {
            await setThemeEmoji(theme, themeEmoji[i]);
        }
    } else {
        for (let i = 0; i < themeEmoji.length; i++) {
            themeEmoji[i].textContent = "🖥️";
        }
    }
    if (!isLoaded) {isLoaded = true}
}

async function setThemeEmoji(value, themeEmoji) {
    if (value === "light") themeEmoji.textContent = "☀️";
    else if (value === "dark") themeEmoji.textContent = "🌙";
    else themeEmoji.textContent = "🔃";
}