import { main } from "./main.js";
import * as theme from "./theme.js";
import * as language from "./language.js";
import {getURL} from "./tools.js";

let isLoaded = true;
export async function loadPage(url) {
    if (!isLoaded) return;
    isLoaded = false;

    try {
        const contentElement = document.getElementById('content');
        contentElement.classList.add("hide");

        // Завантаження сторінки
        const startTime = performance.now();
        const pageUrl = await getURL(url);
        const response = await fetch(pageUrl);

        if (!response.ok) {
            console.error(`Failed to load page: ${url}`);
            return false;
        }

        const endTime = performance.now();
        const executionTime = (endTime - startTime) / 1000;

        // Мінімальний час виконання – 0.025 сек
        if (executionTime < 0.025) {
            const remainingTime = (0.025 - executionTime) * 1000;
            await new Promise(resolve => setTimeout(resolve, remainingTime));
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
        contentElement.innerHTML = '';

        // Додаємо новий контент
        for (const child of Array.from(newContent.childNodes)) {
            contentElement.appendChild(child);
        }

        Promise.all([
            language.loadLocalization(await language.getLanguage()),
            theme.applyTheme(await theme.getTheme()),
            main()
            ]);

        // Оновлення заголовка
        const titleElement = newDocument.querySelector('title');
        document.title = titleElement && titleElement.textContent?.trim() ? titleElement.textContent.trim() : 'Default Title';

        // Оновлення історії
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
