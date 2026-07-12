document.querySelectorAll('[data-toggle]').forEach(sw => {
    sw.addEventListener('click', () => {
        sw.classList.toggle('off');
    });
});

document.getElementById('editProfileBtn').addEventListener('click', () => {
    alert('Edit Profile — cultivation update panel would open here.');
});