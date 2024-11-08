async function updateBackground() {
    try {
        // Отримуємо URL з бекенду FastAPI
        const response = await fetch('/api/background');
        const data = await response.json();

        // Створюємо новий об'єкт Image для попереднього завантаження
        let img = new Image();
        img.src = data.image1k;

        // Коли зображення завантажено повністю, змінюємо фон
        img.onload = () => {
            document.body.style.backgroundImage = `url(${data.image1k})`;
        };
        img.src = data.image2k;
        img.onload = () => {
            document.body.style.backgroundImage = `url(${data.image2k})`;
        };
        img.src = data.image4k;
        img.onload = () => {
            document.body.style.backgroundImage = `url(${data.image4k})`;
        };

    } catch (error) {
        console.error("Помилка при оновленні фону:", error);
    }
}

// Оновлюємо фон кожні 2 хвилини
setInterval(updateBackground, 2 * 60 * 1000); // 2 хвилини = 120000 мс
