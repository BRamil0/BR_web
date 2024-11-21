async function loadPage(url) {
    try {
        await showLoadingBanner();

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

        theme = await getTheme();
        savedLanguage = await getLanguage();

        await applyTheme(theme);
        await loadLocalization(savedLanguage);
        await hideLoadingBanner();
        await sendBrowserInfo();
        await updateCopyTextElements();
        await checkScroll();
        await updateModalButton();
        await updateMessageButton()
        await updateAccountButton();

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
    link.addEventListener('click', async function (event) {
        event.preventDefault();

        const url = this.getAttribute('href');
        await loadPage(url);
    });
});

window.addEventListener('popstate', async function () {
    await loadPage(location.pathname);
});
