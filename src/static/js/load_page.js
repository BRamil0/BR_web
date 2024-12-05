import { main } from "./main.js";
import * as theme from "./theme.js";
import * as language from "./language.js";

export async function loadPage(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            console.error(`Failed to load page: ${url}`);
            return false;
        }

        const html = await response.text();
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;

        const content = tempDiv.querySelector('main#content');
        if (content) {
            document.getElementById('content').innerHTML = content.innerHTML;
        } else {
            console.error('No main content found in the response.');
            return false;
        }
        Promise.all([
            theme.applyTheme(await theme.getTheme()),
            language.loadLocalization(await language.getLanguage()),
            main()
        ]);

        document.title = tempDiv.querySelector('title')?.textContent || 'Default Title';

        history.pushState(null, '', url);
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
