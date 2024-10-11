// Отримуємо всі елементи з класом copy-text
const copyTextElements = document.querySelectorAll('.copy-text');
const copyAlert = document.getElementById('copy-alert');

// Функція для копіювання тексту
function copyToClipboard(text) {
    const tempInput = document.createElement('input');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
}

// Показуємо вікно з повідомленням
function showCopyAlert() {
    const alertBox = document.getElementById('copy-alert');
    alertBox.classList.add('show');

    // Прибираємо спливаюче вікно через 3 секунди
    setTimeout(function() {
        alertBox.classList.remove('show');
    }, 3000);
}

// Додаємо обробник події на кожен елемент
copyTextElements.forEach(element => {
    element.addEventListener('click', () => {
        const text = element.textContent; // Отримуємо текст для копіювання з конкретного елемента
        // Копіюємо текст
        copyToClipboard(text); // Копіюємо текст
        showCopyAlert(); // Показуємо вікно
    });
});

