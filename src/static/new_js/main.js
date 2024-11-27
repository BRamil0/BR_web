import * as loading_banner from "./loading_banner.js";
import * as background from "./background.js";
import * as nav from "./nav.js";
import * as theme from "./theme.js";
import * as language from "./language.js";
import * as copy_text from "./copy_text.js";
import * as cookies from "./cookies.js";

document.addEventListener("DOMContentLoaded", async () => {
    await loading_banner.showLoadingBanner();
    await background.updateBackground();
    await theme.applyTheme(await theme.getTheme());
    await language.loadLocalization(await language.getLanguage());
    await setAccountMenu();
});

window.onload = async () => {
    await nav.updateNavButtons();
    await nav.setThemeMenu()
    await nav.setLanguageMenu();
    await copy_text.updateCopyTextElements();
    await updateModalButton();
    await updateMessageButton()
    await checkScroll();
    await sendBrowserInfo();
    await updateAccountButton();
    while (!background.isLoaded) await new Promise(resolve => setTimeout(resolve, 25));
    await loading_banner.hideLoadingBanner();
};

window.onscroll = async function() {
    if (is_show_navigation_buttons) {
        await checkScroll();
    }
};