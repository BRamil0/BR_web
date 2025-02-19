import * as info_alert from "./info_alert.js";

export async function updateCopyTextElements() {
    const copyTextElements = document.querySelectorAll('.copy-text');
    copyTextElements.forEach(element => {
        if (!element.hasAttribute('data-copy-initialized')) {
            element.addEventListener('click', handleCopyClick);
            element.setAttribute('data-copy-initialized', 'true');
        }
    });
}

async function handleCopyClick(event) {
    const text = event.currentTarget.textContent;
    try {
        await navigator.clipboard.writeText(text);
        await info_alert.showInfoAlert("copy_text_success");
    } catch (error) {
        console.warn('Clipboard API failed, trying fallback...', error);
        const result = await copyToClipboardFallback(text);
        if (result) {
            await info_alert.showInfoAlert("copy_text_success");
        } else {
            console.error('Fallback copying failed.', error);
        }
    }
}

async function copyToClipboardFallback(text) {
    const tempInput = document.createElement('input');
    tempInput.value = text;
    tempInput.setAttribute('readonly', '');
    tempInput.style.position = 'absolute';
    tempInput.style.left = '-9999px';
    document.body.appendChild(tempInput);
    tempInput.select();

    let result = false;
    try {
        result = document.execCommand('copy');
    } catch (error) {
        console.error('Fallback copy failed', error);
    } finally {
        document.body.removeChild(tempInput);
    }
    return result;
}