import * as cookies from "./cookies.js";

export async function getTheme() {
    try {
        const response = await fetch(`/api/default_theme`);
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
    await cookies.setCookie('theme', theme, 7);
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

async function setThemeEmoji(value) {
    if (value === "light") themeEmoji.textContent = "☀️";
    else if (value === "dark") themeEmoji.textContent = "🌙";
    else themeEmoji.textContent = "🔃";
}