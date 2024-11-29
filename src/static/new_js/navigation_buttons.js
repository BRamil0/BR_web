const topButton = document.getElementById("top-button");
const bostonButton = document.getElementById("boston-button");

export let isShowNavigationButtons = true;

export async function checkScroll() {
    if (!isShowNavigationButtons) {
        topButton.classList.remove("show");
        bostonButton.classList.remove("show");
        return;
    }
    const documentHeight = document.documentElement.scrollHeight;
    const windowHeight = window.innerHeight;
    if (documentHeight - 1 > windowHeight) {
        topButton.classList.add("show");
        bostonButton.classList.add("show");
    } else {
        topButton.classList.remove("show");
        bostonButton.classList.remove("show");
    }
}

topButton.addEventListener("click", async () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

bostonButton.addEventListener("click", async () => {
    window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: "smooth"
    });
});