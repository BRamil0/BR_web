import * as language from "./language.js";

export async function showInfoAlert(langKey) {
    const infoAlert = document.getElementById("info-alert");
    let newInfoAlert = infoAlert.cloneNode(true);

    newInfoAlert.id = "info-alert-" + Date.now();
    document.body.appendChild(newInfoAlert);

    let text = await language.getTextForKeyInLanguage(await language.getLanguage(), langKey);
    if (!text) {
        text = langKey;
    }

    newInfoAlert.textContent = text;
    newInfoAlert.classList.add('show');

    setTimeout(() => {
        newInfoAlert.classList.remove('show');
        setTimeout(() => {
            newInfoAlert.remove();
        }, 500);
    }, 3000);
}