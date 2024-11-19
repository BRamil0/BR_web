const accountButtonMenu = document.getElementById("account-button-menu");
const accountMenu = document.getElementById("account-menu");
let is_show_account_menu = true;

async function getCurrentUser() {
    try {
        const response = await fetch("/api/auth/current_user");
        if (!response.ok) {
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return null;
    }
}

async function isAuthenticated() {
    const user = await getCurrentUser();
    return user !== null;
}

async function setAccountMenu() {
    is_show_account_menu = false;
    accountMenu.classList.remove("show");
    setTimeout( async () => {
        if (accountMenu.innerHTML !== "") {
            await delAccountMenu()
        }
        if (await isAuthenticated()) {
            console.log("User is authenticated, showing account menu");
        } else {
            let dataLanguage = await getTextInLanguage(await getLanguage());
            if (!dataLanguage) {
                console.error('dataLanguage is undefined or empty.');
                return false;
            }
            accountMenu.innerHTML += `<a href="/account/login" data-translate="account_login_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_login_button"] || "Авторизація"}</a>`;
            accountMenu.innerHTML += `<a href="/account/register" data-translate="account_register_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_register_button"] || "Реєстрація"}</a>`;
            is_show_account_menu = true;
            return true;
        }
    }, 100);
}

async function delAccountMenu() {
    accountMenu.innerHTML = "";
}

accountButtonMenu.addEventListener("click", async function() {
    if (is_show_account_menu) {
        if (accountMenu.classList.contains("show")) {
            accountMenu.classList.remove("show");
        } else {
            accountMenu.classList.add("show");
        }
    }
});

document.addEventListener("click", async function(event) {
    if (!accountMenu.contains(event.target) && !accountButtonMenu.contains(event.target)) {
        accountMenu.classList.remove("show");
    }
});