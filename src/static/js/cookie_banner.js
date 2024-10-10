// Показати банер, якщо cookie не встановлено
window.addEventListener("load", function() {
    if (!getCookie("cookies_accepted")) {
        document.getElementById("cookie-banner").classList.add("show");
    }
});

// Функція для отримання значення cookie
function getCookie(name) {
    let cookieArr = document.cookie.split(";");

    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

// Встановлення cookie
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Прийняти всі cookie
document.getElementById("accept-cookies").addEventListener("click", function() {
    setCookie("cookies_accepted", "true", 365);
    document.getElementById("cookie-banner").classList.remove("show");
});

// Налаштування cookie (можна реалізувати більш детально)
// document.getElementById("cookie-settings").addEventListener("click", function() {
//     alert("Тут ви можете налаштувати cookie-файли.");
// });
// <button id="cookie-settings" class="cookie-btn">Налаштування cookie</button>