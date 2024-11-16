window.addEventListener("load", async function() {
    if (!await getCookie("cookies_accepted")) {
        document.getElementById("cookie-banner").classList.add("show");
    }
});

document.getElementById("accept-cookies").addEventListener("click", async function() {
    await setCookie("cookies_accepted", "true", 365);
    setTimeout(() => {
        document.getElementById("cookie-banner").classList.remove("show")
    }, 100);
});

// Налаштування cookie (можна реалізувати більш детально)
// document.getElementById("cookie-settings").addEventListener("click", function() {
//     alert("Тут ви можете налаштувати cookie-файли.");
// });
// <button id="cookie-settings" class="cookie-btn">Налаштування cookie</button>