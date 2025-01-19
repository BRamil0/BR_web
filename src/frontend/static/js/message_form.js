import * as modal from "./modal.js";
import * as info_alert from "./info_alert.js";

const formMessageButton = document.getElementsByClassName("form-message-button");
const sendModalMessageButton = document.getElementById("send-modal-message-button");

export async function updateMessageButton() {
    for (let i = 0; i < formMessageButton.length; i++) {
        formMessageButton[i].addEventListener("click", async function (event) {
            const targetId = event.currentTarget.getAttribute("data-target");
            await modal.showModal();
            await modal.showContentModal(targetId);
        });
    }
}

sendModalMessageButton.addEventListener("click", async function () {
    const name = document.getElementById("form-message-name-input").value.trim();
    const author = document.getElementById("form-message-author-input").value.trim();
    const email = document.getElementById("form-message-email-input").value.trim();
    const message = document.getElementById("form-message-input").value.trim();

    if (message === "" || name === "") {
        await info_alert.showInfoAlert("no_required_fields_message_alert");
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
            await info_alert.showInfoAlert("message_alert");
            document.getElementById("form-message-name-input").value = "";
            document.getElementById("form-message-input").value = "";
            await modal.hideContentModal("form-message-modal");
            await modal.hideModal();
        } else {
            console.error("Error:", response.statusText);
            await info_alert.showInfoAlert("error_when_patching_message_alert");
        }
    } catch (error) {
        console.error("Error:", error);
        await info_alert.showInfoAlert("error_when_patching_message_alert");
    }
});