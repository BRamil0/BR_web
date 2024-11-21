const accountButtonMenu = document.getElementById("account-button-menu");
const accountMenu = document.getElementById("account-menu");
let registerButton = document.getElementById("form-register-button");
let loginButton = document.getElementById("form-login-button");
let logoutButton = document.getElementById("form-logout-button");

let is_show_account_menu = true;

async function getCurrentUser() {
    try {
        const response = await fetch("/api/auth/current_user", {
            method: "GET",
            credentials: "same-origin",
        });
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
        let dataLanguage = await getTextInLanguage(await getLanguage());
            if (!dataLanguage) {
                console.error('dataLanguage is undefined or empty.');
                return false;
            }
        if (await isAuthenticated()) {
            accountMenu.innerHTML += `<a href="/account/profile" data-translate="account_profile_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_profile_button"] || "Профіль"}</a>`;
            accountMenu.innerHTML += `<a href="/account/settings" data-translate="account_settings_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_settings_button"] || "Налаштування"}</a>`;
            accountMenu.innerHTML += `<button id="form-logout-button" data-translate="account_logout_button" class="jetbrains-mono-br">${dataLanguage["account_logout_button"] || "Вихід"}</button>`;
            is_show_account_menu = true;
            await updateAccountButton();
            return true
        } else {
            accountMenu.innerHTML += `<a href="/account/login" data-translate="account_login_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_login_button"] || "Авторизація"}</a>`;
            accountMenu.innerHTML += `<a href="/account/register" data-translate="account_register_button" class="link a-button jetbrains-mono-br">${dataLanguage["account_register_button"] || "Реєстрація"}</a>`;
            is_show_account_menu = true;
            return true;
        }
    }, 50);
}

async function delAccountMenu() {
    accountMenu.innerHTML = "";
}

async function registerAccount(username, email, password) {
    try {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username.value,
                email: email.value,
                password: password.value,
            }),
        });
        if (!response.ok) {
            console.log(response.json());
            await showInfoAlert("register_error_cannot_register");
            return false
        }
        username.value = "";
        email.value = "";
        password.value = "";
        window.location.href = "/account/profile/my";
        return true
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        await showInfoAlert("register_error_cannot_register");
        return false
    }
}

async function loginAccount(email, password) {
    try {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email.value,
                password: password.value,
            }),
        });
        if (!response.ok) {
            await showInfoAlert("login_error_cannot_login");
            return false
        }
        email.value = "";
        password.value = "";
        window.location.href = "/account/profile/my";
        return true
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        await showInfoAlert("login_error_cannot_login");
        return false
    }
}

async function logoutAccount() {
    try {
        const response = await fetch("/api/auth/logout");
        if (!response.ok) {
            await showInfoAlert("logout_error_cannot_logout");
            return false
        }
        await showInfoAlert("logout_success_logout");
        window.location.href = "/";
        return true
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        await showInfoAlert("logout_error_cannot_logout");
        return false
    }
}

async function dataVerification(username = null, email, password, password2 = null) {
    const cleanInput = (input) => input.replace(/<[^>]*>?/gm, '');
    if (username !== null) {
        if (username.value === "") {
            username.style.borderColor = "red";
        }
    }
    if (email.value === "") {
        email.style.borderColor = "red";
    }
    if (password.value === "") {
        password.style.borderColor = "red";
        if (password2 !== null) {
            password2.style.borderColor = "red";
        }
        await showInfoAlert("register_error_empty_fields");
        setTimeout(() => {
            if (username !== null) {
                username.style.borderColor = "";
            }
            email.style.borderColor = "";
            password.style.borderColor = "";
            if (password2 !== null) {
                password2.style.borderColor = "";
            }
        }, 1000);
        return false
    }

    if (username !== null) {
        if (cleanInput(username.value) !== username.value || !await validateUsername(username.value) || username.length > 128 || username.length < 2) {
            username.style.borderColor = "red";
            await showInfoAlert("register_error_invalid_username");
            setTimeout(() => {
                username.style.borderColor = "";
            })
            return false
        }
    }

    if (cleanInput(email.value) !== email.value || !await validateEmail(email.value)) {
        email.style.borderColor = "red";
        await showInfoAlert("register_error_invalid_email");
        setTimeout(() => {
            email.style.borderColor = "";
        })
        return false
    }

    if (cleanInput(password.value) !== password.value || !await validatePassword(password.value) || password.length > 128 || password.length < 8) {
        password.style.borderColor = "red";
        await showInfoAlert("register_error_invalid_password");
        setTimeout(() => {
            password.style.borderColor = "";
        })
        return false
    }
    if (password2 !== null) {
        if (password.value !== password.value) {
            password.style.borderColor = "red";
            password2.style.borderColor = "red";
            await showInfoAlert("register_error_passwords_not_match");
            setTimeout(() => {
                password.style.borderColor = "";
                password2.style.borderColor = "";
            }, 1000);
            return false
        }
    }

    return true
}

async function validateUsername(username) {
    const pattern = /^[a-zA-Zа-яА-Я0-9_.\-+~?,:{}=&|`[\]]{2,128}$/;
    return pattern.test(username);
}

async function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

async function validatePassword(password) {
    const pattern = /^(?=.*[a-zA-Zа-яА-Я])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>+=]).{6,128}$/;
    return pattern.test(password);
}

async function updateAccountButton() {
    registerButton = document.getElementById("form-register-button");
    loginButton = document.getElementById("form-login-button");
    logoutButton = document.getElementById("form-logout-button");
    console.log(registerButton, loginButton, logoutButton);

    if (registerButton !== null) {
        registerButton.addEventListener("click", async function (event) {
            event.preventDefault();
            const username = document.getElementById("form-register-username-input");
            const email = document.getElementById("form-register-email-input");
            const password = document.getElementById("form-register-password-input");
            const password2 = document.getElementById("form-register-password2-input");
            if (await dataVerification(username, email, password, password2)) {
                if (await registerAccount(username, email, password)) {
                    await showInfoAlert("register_success_register");
                }
            }
        });
    }

    if (loginButton !== null) {
        loginButton.addEventListener("click", async function (event) {
            event.preventDefault();
            const email = document.getElementById("form-login-email-input");
            const password = document.getElementById("form-login-password-input");
            console.log(email, password);
            if (await dataVerification(null, email, password, null)) {
                if (await loginAccount(email, password)) {
                    await showInfoAlert("login_success_login");
                }
            }
        });
    }

    if (logoutButton !== null) {
        logoutButton.addEventListener("click", async function(event) {
            event.preventDefault();
            if (await logoutAccount()) {
                await showInfoAlert("logout_success_logout");
            }
        });
    }
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