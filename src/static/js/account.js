import {showInfoAlert} from "./info_alert.js";
import {setAccountMenu} from "./nav.js";
import {loadPage} from "./load_page.js";

let registerButton = document.getElementById("form-register-button");
let loginButton = document.getElementById("form-login-button");
let logoutButton = document.getElementById("form-logout-button");

export async function getCurrentUser() {
    try {
        const response = await fetch("/api/auth/current_user", {
            method: "GET",
            credentials: "same-origin",
        });
        if (!response.ok) {
            return null;
        }
        let data = await response.json();
        if (data["status"] !== null) {
            return data;
        }
        return null;
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        return null;
    }
}

export async function isAuthenticated(user) {
    return user !== null;
}

export async function registerAccount(username, email, password) {
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
        await loadPage("/account/profile/my");
        return true
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        await showInfoAlert("register_error_cannot_register");
        return false
    }
}

export async function loginAccount(email, password) {
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
        await loadPage("/account/profile/my");
        return true
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        await showInfoAlert("login_error_cannot_login");
        return false
    }
}

export async function logoutAccount() {
    try {
        const response = await fetch("/api/auth/logout");
        if (!response.ok) {
            await showInfoAlert("logout_error_cannot_logout");
            return false
        }
        await showInfoAlert("logout_success_logout");
        await loadPage("/");
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

export async function updateAccountButton() {
    registerButton = document.getElementById("form-register-button");
    loginButton = document.getElementById("form-login-button");
    logoutButton = document.getElementById("form-logout-button");

    if (registerButton !== null) {
        registerButton.addEventListener("click", async function (event) {
            event.preventDefault();
            const username = document.getElementById("form-register-username-input");
            const email = document.getElementById("form-register-email-input");
            const password = document.getElementById("form-register-password-input");
            const password2 = document.getElementById("form-register-password2-input");
            if (await dataVerification(username, email, password, password2)) {
                if (await registerAccount(username, email, password)) {
                    await setAccountMenu();
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
            if (await loginAccount(email, password)) {
                await setAccountMenu();
                await showInfoAlert("login_success_login");
            }
        });
    }
}
