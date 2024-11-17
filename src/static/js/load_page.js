async function loadPage(url) {
    try {
        await showLoadingBanner();

        const response = await fetch(url);
        if (!response.ok) {
            console.error(`Failed to load page: ${url}`);
            return false;
        }

        const html = await response.text(); // Отримуємо весь HTML контент
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;

        const content = tempDiv.querySelector('main#content');
        if (content) {
            document.getElementById('content').innerHTML = content.innerHTML;
        } else {
            console.error('No main content found in the response.');
            return false;
        }

        theme = await getTheme();
        savedLanguage = await getLanguage();
        await updateCopyTextElements();
        await applyTheme(theme);
        await loadLocalization(savedLanguage);
        await sendBrowserInfo();
        await checkScroll();

        document.title = tempDiv.querySelector('title')?.textContent || 'Default Title';

        history.pushState(null, '', url);
        return true;
    } catch (error) {
        console.error('Error loading page:', error);
        return false;
    } finally {
        await hideLoadingBanner();
    }
}

document.querySelectorAll('.link').forEach(link => {
    link.addEventListener('click', async function (e) {
        e.preventDefault(); // Запобігаємо стандартному переходу

        const url = this.getAttribute('href'); // Отримуємо URL посилання
        await loadPage(url); // Викликаємо функцію для завантаження контенту
    });
});

window.addEventListener('popstate', async function () {
    await loadPage(location.pathname);
});
