const formButton = document.getElementsByClassName("form-button");
const modal = document.getElementById("modal");
const closeModalButton = document.getElementById("close-modal");
const sendMessageButton = document.getElementById("send-message-button");
const messageInput = document.getElementById("message-input");
const nameInput = document.getElementById("name-input");
const errorMessage = document.getElementById("error-message");
const messageAuthor = document.getElementById("message-author-input");
const messageEmail = document.getElementById("message-email-input");

async function showModal() {
    modal.style.display = "block";
    await new Promise(resolve => setTimeout(resolve, 100));
    modal.style.visibility = "visible";
    modal.style.opacity = "1";
}

async function hideModal() {
    modal.style.visibility = "hidden";
    modal.style.opacity = "0";
    await new Promise(resolve => setTimeout(resolve, 325));
    modal.style.display = "none";
    errorMessage.textContent = "";
}

async function handleOutsideClick(event) {
    if (event.target === modal) {
        await hideModal();
    }
}

async function showMessageAlert() {
    const infoAlert = document.getElementById("info-alert");
    infoAlert.textContent = await getTextForKeyInLanguage(await getLanguage(), "message_alert");
    infoAlert.classList.add('show');
    setTimeout(() => {
        infoAlert.classList.remove('show');
    }, 3000);
}

Array.from(formButton).forEach(button => {
    button.addEventListener("click", showModal);
});

closeModalButton.addEventListener("click", hideModal);
window.addEventListener("click", handleOutsideClick);

sendMessageButton.addEventListener("click", async function () {
    const message = messageInput.value.trim();
    const name = nameInput.value.trim();
    const email = messageEmail.value.trim();
    const author = messageAuthor.value.trim();

    if (message === "" || name === "") {
        errorMessage.textContent = "Будь ласка, введіть повідомлення";
        return;
    }

    const data = {
        name,
        message,
        email,
        author,
    };

    try {
        const response = await fetch('/api/telegram/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            await showMessageAlert();
            errorMessage.textContent = "";
            messageInput.value = "";
            nameInput.value = "";
            await hideModal();
        } else {
            console.error("Error:", response.statusText);
            errorMessage.textContent = "Помилка відправки повідомлення";
        }
    } catch (error) {
        console.error("Error:", error);
        errorMessage.textContent = "Виникла помилка при відправці";
    }
});