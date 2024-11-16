async function updateBackground() {
    try {
        const response = await fetch('/api/background');
        if (!response.ok) {
            console.error("Error fetching background URL");
            return false;
        }
        const data = await response.json();

        const imageUrls = [data["image1k"], data["image2k"], data["image4k"]];

        for (const url of imageUrls) {
            const img = new Image();
            img.src = url;

            await new Promise((resolve, reject) => {
                img.onload = resolve;
                img.onerror = reject;
            });

            document.body.style.backgroundImage = `url(${url})`;
        }
        return true;
    } catch (error) {
        console.error("Error updating background:", error);
        return false;
    }
}

// Оновлюємо фон кожні 2 хвилини
setInterval(updateBackground, 2 * 60 * 1000);
