let loadedFullHD = false;
let loaded2k = false;
let loaded4k = false;
let currentImageQuality = 'FullHD';

export let isLoaded = false;

setInterval(async () => {
    await updateBackground();
}, 2 * 60 * 1000);

export async function updateBackground() {

    try {
        const response = await fetch('/api/background');
        if (!response.ok) {
            console.error("Error fetching background URL");
            return false;
        }

        const { image1k, image2k, image4k } = await response.json();
        const imageUrls = {
            'FullHD': image1k,
            '2k': image2k,
            '4k': image4k
        };

        if (!loadedFullHD) {
            await loadImage(imageUrls.FullHD);
            loadedFullHD = true;
            document.body.style.backgroundImage = `url(${imageUrls.FullHD})`;
            if (!isLoaded) isLoaded = true;
        } else if (!loaded2k && currentImageQuality === 'FullHD') {
            await loadImage(imageUrls['2k']);
            loaded2k = true;
            document.body.style.backgroundImage = `url(${imageUrls['2k']})`;
            currentImageQuality = '2k';
        } else if (!loaded4k && currentImageQuality === '2k') {
            await loadImage(imageUrls['4k']);
            loaded4k = true;
            document.body.style.backgroundImage = `url(${imageUrls['4k']})`;
            currentImageQuality = '4k';
        }

        return true;
    } catch (error) {
        console.error("Error updating background:", error);
        return false;
    }
}

async function loadImage(url) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = url;
        img.onload = () => resolve();
        img.onerror = () => reject(new Error(`Failed to load image: ${url}`));
    });
}
