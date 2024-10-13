async function updateBackground() {
    try {
        // Отримуємо URL з бекенду FastAPI
        const response = await fetch('/background');
        const data = await response.json();

        // Оновлюємо background-image для body
        document.body.style.backgroundImage = `url(${data.image})`;
    } catch (error) {
        console.error("Помилка при оновленні фону:", error);
    }
}

// Оновлюємо фон кожні 2 хвилини
setInterval(updateBackground, 2 * 60 * 1000); // 2 хвилини = 120000 мс
