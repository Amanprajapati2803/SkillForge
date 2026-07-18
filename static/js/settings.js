document.querySelectorAll('[data-toggle]').forEach(sw => {
    sw.addEventListener('click', () => {
        sw.classList.toggle('off');
    });
});

const editModal = document.getElementById("editProfileModal");

document.getElementById("editProfileBtn").addEventListener("click", () => {
    editModal.classList.remove("hidden");
});

document.getElementById("closeEditModal").addEventListener("click", () => {
    editModal.classList.add("hidden");
});