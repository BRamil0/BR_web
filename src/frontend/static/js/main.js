import * as loading_banner from "./loading_banner.js";
import * as background from "./background.js";
import * as nav from "./nav.js";
import * as theme from "./theme.js";
import * as language from "./language.js";
import * as account from "./account.js";
import * as copy_text from "./copy_text.js";
import * as navigation_buttons from "./navigation_buttons.js";
import * as informant from "./informant.js";
import * as modal from "./modal.js";
import * as message_form from "./message_form.js";
import * as load_page from "./load_page.js";
import "./cookie_banner.js";

export async function main() {
    await nav.updateNavButtons();
    await account.updateAccountButton();
    await load_page.updateLinkClicks();
    await copy_text.updateCopyTextElements();
    await navigation_buttons.checkScroll();
    await informant.sendingDataToInformant();
    await modal.updateModalButton();
    await message_form.updateMessageButton();
}

document.addEventListener("DOMContentLoaded", async () => {
    Promise.all([
        loading_banner.showLoadingBanner(),
        background.updateBackground(),
        theme.applyTheme(await theme.getTheme()),
        language.loadLocalization(await language.getLanguage()),
        nav.setThemeMenu(),
        nav.setLanguageMenu(),
        nav.setAccountMenu(),
    ]);
    while (!background.isLoaded || !language.isLoaded || !theme.isLoaded) {
        await new Promise(resolve => setTimeout(resolve, 5));
    }
    await loading_banner.hideLoadingBanner();
});

window.onload = async () => {
    await main();
};

window.onscroll = async function() {
    if (navigation_buttons.isShowNavigationButtons) {
        await navigation_buttons.checkScroll();
    }
};

document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', async function() {
        this.classList.add('button-active');

        setTimeout(() => {
            this.classList.remove('button-active');
        }, 1000); //
    });
});