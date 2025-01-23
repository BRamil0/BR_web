import { main } from "./main.js";
import * as theme from "./theme.js";
import * as language from "./language.js";

let isLoaded = true;
export async function loadPage(url) {
    if (!isLoaded) {return}
    isLoaded = false;
    try {
        const contentElement = document.getElementById('content');
        contentElement.classList.add("hide");

        // Завантажуємо сторінку
        const startTime = performance.now();
        const response = await fetch(url);
        if (!response.ok) {
            console.error(`Failed to load page: ${url}`);
            return false;
        }
        const endTime = performance.now();
        const executionTime = (endTime - startTime) / 1000;
        if (executionTime < 0.025) {
            const remainingTime = 0.025 - executionTime;
            setTimeout(() => {}, remainingTime);
        }

        const html = await response.text();

        // Парсимо HTML
        const parser = new DOMParser();
        const newDocument = parser.parseFromString(html, 'text/html');

        const newContent = newDocument.querySelector('main#content');
        if (!newContent) {
            console.error('No main content found in the response.');
            return false;
        }

        // Очищуємо поточний контент
        while (contentElement.firstChild) {
            contentElement.removeChild(contentElement.firstChild);
        }

        // Додаємо новий контент до реального DOM
        for (const child of Array.from(newContent.childNodes)) {
            contentElement.appendChild(child);
        }

        // Завантажуємо локалізацію вже для нового контенту
        const languageCode = await language.getLanguage();
        await language.loadLocalization(languageCode);

        // Завантажуємо тему
        const themeName = await theme.getTheme();
        await theme.applyTheme(themeName);

        // Виконуємо основні скрипти
        await main();

        // Оновлюємо заголовок
        document.title = newDocument.querySelector('title')?.textContent || 'Default Title';

        // Оновлюємо історію
        history.pushState(null, '', url);

        // Показуємо контент після всіх змін
        contentElement.classList.remove("hide");
        isLoaded = true;
        return true;
    } catch (error) {
        console.error('Error loading page:', error);
        return false;
    }
}



async function handlePopstate() {
    await loadPage(location.pathname);
}

export async function updateLinkClicks() {
    document.querySelectorAll('.link').forEach(link => {
        const clonedLink = link.cloneNode(true);
        link.replaceWith(clonedLink);
        clonedLink.addEventListener('click', async function (event) {
            event.preventDefault();

            const url = this.getAttribute('href');
            if (url) {
                await loadPage(url);
            }
        });
    });

    window.removeEventListener('popstate', handlePopstate);
    window.addEventListener('popstate', handlePopstate);
}

window.addEventListener('popstate', async function () {
    await loadPage(location.pathname);
});
