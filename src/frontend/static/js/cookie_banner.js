import * as cookie from "./cookies.js";

window.addEventListener("load", async function() {
    if (!await cookie.getCookie("cookies_accepted")) {
        document.getElementById("cookie-banner").classList.add("show");
    }
});

document.getElementById("accept-cookies").addEventListener("click", async function() {
    await cookie.setCookie("cookies_accepted", "true", 365);
    setTimeout(() => {
        document.getElementById("cookie-banner").classList.remove("show")
    }, 100);
});