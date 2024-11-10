const formButton = document.getElementsByClassName("form-button");
const modal = document.getElementById("modal");
const closeModalButton = document.getElementById("close-modal");
const sendMessageButton = document.getElementById("send-message-button");
const messageInput = document.getElementById("message-input");
const nameInput = document.getElementById("name-input");
const errorMessage = document.getElementById("error-message");
const messageAuthor = document.getElementById("message-author-input");
const messageEmail = document.getElementById("message-email-input");


for (let i = 0; i < formButton.length; i++) {
    formButton[i].addEventListener("click", function() {
        modal.style.display = "block";
        setTimeout(() => {
                modal.style.visibility = "visible";
                modal.style.opacity = "1";
            }, 100);
    });
}

closeModalButton.addEventListener("click", function() {
    modal.style.visibility = "hidden";
    modal.style.opacity = "0";
    setTimeout(() => {
        modal.style.display = "none";
        errorMessage.textContent = "";
        }, 325);
});

window.addEventListener("click", function(event) {
    if (event.target === modal) {
        modal.style.visibility = "hidden";
        modal.style.opacity = "0";
        setTimeout(() => {
            modal.style.display = "none";
            errorMessage.textContent = "";
            }, 325);
    }
});

function showMessageAlert() {
    const alertBox = document.getElementById("message-alert");
    alertBox.classList.add('show');

    setTimeout(function() {
        alertBox.classList.remove('show');
    }, 3000);
}

sendMessageButton.addEventListener("click", async function() {
    const message = messageInput.value;
    const name = nameInput.value;
    const email = messageEmail.value;
    const author = messageAuthor.value;

    if (message.trim() === "" || name.trim() === "") {
        errorMessage.textContent = "Будь ласка, введіть повідомлення";
        return;
    }

    const data = {
        name: name,
        message: message,
        email: email,
        author: author
    };

    try {
        const response = await fetch('/api/telegram/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showMessageAlert();
            errorMessage.textContent = "";
            messageInput.value = "";
            nameInput.value = "";
            modal.style.visibility = "hidden";
            modal.style.opacity = "0";
            setTimeout(() => {
                modal.style.display = "none";
                }, 325);
        } else {
            console.error("Error:", response.statusText);
            errorMessage.textContent = "Помилка відправки повідомлення";
        }
    } catch (error) {
        console.error("Error:", error);
        errorMessage.textContent = "Виникла помилка при відправці";
    }
});