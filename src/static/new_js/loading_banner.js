const loadingBanner = document.getElementById('loading-banner');
let textBanner = [];
for (let i = 0; i < 3; i++) {
    textBanner[i] = document.getElementById(`loading-banner-text-${i + 1}`);
}

let timeout = [];
export async function showLoadingBanner() {
    let timeTnt = 2000;
    loadingBanner.classList.remove('hidden');

    for (let i = 0; i < textBanner.length; i++) {
        textBanner[i].classList.add('show');
        await new Promise(resolve => {timeout[i] = setTimeout(() => {resolve();}, timeTnt);});
        timeTnt *= 2;
        textBanner[i].classList.remove('show');
    }
}

export async function hideLoadingBanner() {
    loadingBanner.classList.remove('show');
    for (let i = 0; i < textBanner.length; i++) {
        if (!timeout[i]) continue;
        clearTimeout(timeout[i]);
        textBanner[i].classList.remove('show');
    }
}