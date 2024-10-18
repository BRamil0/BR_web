async function loadPage(url) {
    try {
        showLoadingBanner(); // Показуємо банер
        const response = await fetch(url); // Отримуємо новий контент
        if (!response.ok) {
            throw new Error("Не вдалося завантажити сторінку");
        }
        const html = await response.text(); // Отримуємо весь HTML контент

        // Створюємо тимчасовий DOM-елемент для видобутку вмісту з <main>
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html; // Поміщаємо весь HTML в тимчасовий елемент

        // Витягуємо вміст з <main class="main" id="content">
        const newContent = tempDiv.querySelector('main#content').innerHTML;

        // Заміна вмісту
        document.getElementById('content').innerHTML = newContent;

        // Продовжуємо з іншими функціями, такими як applyTheme, loadLocalization, etc.
        const theme = getCookie('theme') || 'system';
        const savedLanguage = getCookie('language') || 'ukr'; // Встановити мову за замовчуванням
        applyTheme(theme);
        loadLocalization(savedLanguage);
        await sendBrowserInfo();

        // Оновлення історії браузера
        history.pushState(null, '', url);
        console.log("Сторінка завантажена!")
    } catch (error) {
        console.error("Помилка:", error);
    } finally {
        hideLoadingBanner(); // Прибираємо банер
    }
}

document.querySelectorAll('.link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault(); // Запобігаємо стандартному переходу

        const url = this.getAttribute('href'); // Отримуємо URL посилання
        loadPage(url); // Викликаємо функцію для завантаження контенту
    });
});

// Для підтримки кнопки "Назад" або "Вперед"
window.addEventListener('popstate', function () {
    loadPage(location.pathname); // Завантажуємо сторінку при зміні історії
});
