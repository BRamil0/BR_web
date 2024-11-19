const formMessageButton = document.getElementsByClassName("form-message-button");
const sendModalMessageButton = document.getElementById("send-modal-message-button");

async function updateMessageButton() {
    for (let i = 0; i < formMessageButton.length; i++) {
        formMessageButton[i].addEventListener("click", async function (event) {
            const targetId = event.currentTarget.getAttribute("data-target");
            await showModal();
            await showContentModal(targetId);
        });
    }
}

sendModalMessageButton.addEventListener("click", async function () {
    const name = document.getElementById("form-message-name-input").value.trim();
    const author = document.getElementById("form-message-author-input").value.trim();
    const email = document.getElementById("form-message-email-input").value.trim();
    const message = document.getElementById("form-message-input").value.trim();

    if (message === "" || name === "") {
        await showInfoAlert("no_required_fields_message_alert");
        document.getElementById("form-message-name-input").style.borderColor = "red";
        document.getElementById("form-message-input").style.borderColor = "red";
        setTimeout(() => {
            document.getElementById("form-message-name-input").style.borderColor = null;
            document.getElementById("form-message-input").style.borderColor = null
        }, 3000);
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
            await showInfoAlert("message_alert");
            document.getElementById("form-message-name-input").value = "";
            document.getElementById("form-message-input").value = "";
            await hideContentModal("form-message-modal");
            await hideModal();
        } else {
            console.error("Error:", response.statusText);
            await showInfoAlert("error_when_patching_message_alert");
        }
    } catch (error) {
        console.error("Error:", error);
        await showInfoAlert("error_when_patching_message_alert");
    }
});