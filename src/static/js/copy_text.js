let copyTextElements = document.querySelectorAll('.copy-text');

async function updateCopyTextElements() {
    copyTextElements = document.querySelectorAll('.copy-text');
    for (const element of copyTextElements) {
        element.addEventListener('click', async () => {
            const text = element.textContent;
            await copyToClipboard(text);
            await showInfoAlert("copy_alert");
        });
    }
}

async function copyToClipboard(text) {
    const tempInput = document.createElement('input');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    try {
        await navigator.clipboard.writeText(text);
    } catch (error) {
        console.error('Copying text failed', error);
    }
    document.body.removeChild(tempInput);
}