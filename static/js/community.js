  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('[data-fade]').forEach(el => observer.observe(el));
  // ================= CREATE DISCUSSION MODAL =================

const discussionModal = document.getElementById("discussionModal");

const openDiscussionModal = document.getElementById("openDiscussionModal");

const closeDiscussionModal = document.getElementById("closeDiscussionModal");

const cancelDiscussionModal = document.getElementById("cancelDiscussionModal");

openDiscussionModal.addEventListener("click", () => {
    discussionModal.classList.remove("hidden");
    discussionModal.classList.add("flex");
});

function closeModal() {
    discussionModal.classList.remove("flex");
    discussionModal.classList.add("hidden");
}

closeDiscussionModal.addEventListener("click", closeModal);

cancelDiscussionModal.addEventListener("click", closeModal);

discussionModal.addEventListener("click", (e) => {
    if (e.target === discussionModal) {
        closeModal();
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeModal();
    }
});

const imageInput = document.getElementById("imageInput");
const imageName = document.getElementById("imageName");

imageInput.addEventListener("change", () => {

    imageName.textContent =
        imageInput.files.length
            ? imageInput.files[0].name
            : "No image selected";

});

const attachmentInput = document.getElementById("attachmentInput");
const attachmentName = document.getElementById("attachmentName");

attachmentInput.addEventListener("change", () => {

    attachmentName.textContent =
        attachmentInput.files.length
            ? attachmentInput.files[0].name
            : "No attachment selected";

});

const postDetailPanel = document.getElementById("postDetailPanel");

const postDetailTitle = document.getElementById("postDetailTitle");
const postDetailAuthor = document.getElementById("postDetailAuthor");
const postDetailCategory = document.getElementById("postDetailCategory");
const postDetailDate = document.getElementById("postDetailDate");
const postDetailContent = document.getElementById("postDetailContent");

const closePostDetail = document.getElementById("closePostDetail");

document.querySelectorAll(".post-row").forEach(post => {

    post.addEventListener("click", function(e){

        e.preventDefault();

        postDetailTitle.textContent = this.dataset.title;
        postDetailAuthor.textContent = this.dataset.author;
        postDetailCategory.textContent = this.dataset.category;
        postDetailDate.textContent = this.dataset.date;
        postDetailContent.textContent = this.dataset.content;

        postDetailPanel.classList.remove("hidden");

        postDetailPanel.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    });

});

closePostDetail.addEventListener("click", function(){

    postDetailPanel.classList.add("hidden");

});

document.querySelectorAll(".like-btn").forEach(button => {

    button.addEventListener("click", async function () {

        const postId = this.dataset.postId;

        const response = await fetch(`/community/post/${postId}/like`, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        const data = await response.json();

        this.querySelector(".like-count").textContent = data.like_count;

        const icon = this.querySelector(".like-icon");

        if (data.liked) {
            icon.setAttribute("fill", "currentColor");
        } else {
            icon.setAttribute("fill", "none");
        }

        this.dataset.liked = data.liked;

    });

});