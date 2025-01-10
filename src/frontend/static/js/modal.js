const modal = document.getElementById("modal");
const closeModalButton = document.getElementsByClassName("close-modal-button");

export async function showModal() {
    modal.style.display = "block";
    await new Promise(resolve => setTimeout(resolve, 100));
    modal.classList.add("show")
}

export async function hideModal() {
    const contentModals = modal.querySelectorAll(".modal-content");
    const hasVisibleContent = Array.from(contentModals).some(content => content.classList.contains("show"));

    if (!hasVisibleContent) {
        modal.classList.remove("show");
        await new Promise(resolve => setTimeout(resolve, 100));
        modal.style.display = "none";
    }
}
export async function showContentModal(id) {
    let contentModal = document.getElementById(id);
    console.log(contentModal);
    contentModal.classList.add("show")
}

export async function hideContentModal(id) {
    let contentModal = document.getElementById(id);
    console.log(contentModal);
    contentModal.classList.remove("show")
}

window.addEventListener("click", async (event) => {
    if (event.target === modal) {
        await hideModal();
    }
});

export async function updateModalButton() {
    for (let i = 0; i < closeModalButton.length; i++) {
        closeModalButton[i].addEventListener("click", async function (event) {
            const contentId = event.target.closest(".modal-content").id;
            await hideContentModal(contentId);
            await hideModal();
        });
    }
}