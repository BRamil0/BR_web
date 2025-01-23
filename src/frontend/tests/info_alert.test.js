import { showInfoAlert } from '../../static/js/info_alert.js';
import * as language from '../../static/js/language.js';

jest.mock('../../static/js/language', () => ({
    getTextForKeyInLanguage: jest.fn(),
    getLanguage: jest.fn()
}));

describe('showInfoAlert', () => {
    let originalBody;

    beforeAll(() => {
        // Зберігаємо оригінальне значення document.body, щоб після тесту не було змін
        originalBody = document.body;
    });

    beforeEach(() => {
        // Очищаємо DOM перед кожним тестом
        document.body.innerHTML = `<div id="info-alert"></div>`;
    });

    afterAll(() => {
        // Відновлюємо оригінальне значення document.body після всіх тестів
        document.body = originalBody;
    });

    test('should add a new info alert with correct text', async () => {
        // Мокаємо getLanguage і getTextForKeyInLanguage для передбачуваного результату
        language.getLanguage.mockResolvedValue('en');  // Мокаємо результат getLanguage
        language.getTextForKeyInLanguage.mockResolvedValue('Info alert text');  // Мокаємо результат getTextForKeyInLanguage

        // Викликаємо функцію
        await showInfoAlert('alert_key');

        // Перевіряємо, чи додано новий елемент в DOM
        const newAlert = document.getElementById('info-alert-');
        expect(newAlert).toBeInTheDocument();  // Перевіряємо, що елемент є в DOM

        // Перевіряємо текст в новому елементі
        expect(newAlert.textContent).toBe('Info alert text');

        // Перевіряємо, чи був доданий клас 'show'
        expect(newAlert.classList.contains('show')).toBe(true);

        // Симулюємо час для перевірки видалення класу
        jest.advanceTimersByTime(3000);  // Прокачуємо час на 3 секунди
        expect(newAlert.classList.contains('show')).toBe(false);  // Клас 'show' повинен бути видалений

        // Перевіряємо, чи елемент був видалений з DOM
        jest.advanceTimersByTime(500);  // Час для видалення елемента
        expect(newAlert.parentElement).toBeNull();  // Елемент має бути видалений
    });

    test('should use langKey as text if no translation found', async () => {
        language.getLanguage.mockResolvedValue('en');
        language.getTextForKeyInLanguage.mockResolvedValue(null);  // Якщо текст не знайдений

        await showInfoAlert('alert_key');

        const newAlert = document.getElementById('info-alert-');
        expect(newAlert.textContent).toBe('alert_key');  // Має бути текст langKey, оскільки переклад не знайдений
    });
});
