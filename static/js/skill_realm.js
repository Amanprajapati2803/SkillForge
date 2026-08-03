/** learning session **/

function openSessionModal() {
    document
        .getElementById("sessionModal")
        .classList.remove("hidden");

    document
        .getElementById("sessionModal")
        .classList.add("flex");
}

function closeSessionModal() {
    document
        .getElementById("sessionModal")
        .classList.remove("flex");

    document
        .getElementById("sessionModal")
        .classList.add("hidden");
}


/** edit button scripting**/
function openEditSessionModal(button) {

    document.getElementById("editSessionForm").action =
        `/session/${button.dataset.id}/edit`;

    document.getElementById("editSessionTitle").value =
        button.dataset.title;

    document.getElementById("editSessionDuration").value =
        button.dataset.duration;

    document.getElementById("editSessionNotes").value =
        button.dataset.notes;

    document.getElementById("editSessionModal").classList.remove("hidden");
    document.getElementById("editSessionModal").classList.add("flex");
}



const searchInput = document.getElementById("resourceSearch");

const clearSearch =
    document.getElementById("clearSearch");

const clearFilters =
    document.getElementById("clearFilters");

const sortFilter =
    document.getElementById("resourceSort");

const typeFilter = document.getElementById("resourceTypeFilter");

const difficultyFilter = document.getElementById("difficultyFilter");


const cards = [...document.querySelectorAll(".resource-card")]; /*list of all resource cards*/

const resourceGrid =
    document.getElementById("resourceGrid"); /* grid container for all resource cards */

const resourceCount = document.getElementById("resourceCount");

const totalResources = cards.length;

const noResourcesMessage =
    document.getElementById("noResourcesMessage");

function filterResources() {

    const search =
        searchInput.value.toLowerCase().trim();

    const type =
        typeFilter.value.toLowerCase();

    const difficulty =
        difficultyFilter.value.toLowerCase();

    let visibleCount = 0;

    cards.forEach(card => {

        const title = card.dataset.title;
        const description = card.dataset.description;
        const cardType = card.dataset.type;
        const cardDifficulty = card.dataset.difficulty;

        const matchesSearch =
            title.includes(search) ||
            description.includes(search);

        const matchesType =
            type === "all" ||
            cardType === type;

        const matchesDifficulty =
            difficulty === "all" ||
            cardDifficulty === difficulty;

        if (
            matchesSearch &&
            matchesType &&
            matchesDifficulty
        ) {

            card.classList.remove("opacity-0");

            card.style.display = "";

            visibleCount++;

        } else {

            card.classList.add("opacity-0");

            setTimeout(() => {

                card.style.display = "none";

            }, 180);

        }

    });

    resourceCount.textContent =
        `Showing ${visibleCount} of ${totalResources} Resources`;

    if (noResourcesMessage) {

        if (visibleCount === 0) {
            noResourcesMessage.classList.remove("hidden");
        } else {
            noResourcesMessage.classList.add("hidden");
        }

    }

    if (searchInput.value.trim() === "") {

        clearSearch.classList.add("hidden");

    } else {

        clearSearch.classList.remove("hidden");

    }


    const sortValue = sortFilter.value;

    const difficultyOrder = {
        beginner: 1,
        intermediate: 2,
        advanced: 3
    };

    cards.sort((a, b) => {

        if (sortValue === "title") {

            return a.dataset.title.localeCompare(b.dataset.title);

        }

        if (sortValue === "beginner") {

            return (
                difficultyOrder[a.dataset.difficulty] -
                difficultyOrder[b.dataset.difficulty]
            );

        }

        if (sortValue === "advanced") {

            return (
                difficultyOrder[b.dataset.difficulty] -
                difficultyOrder[a.dataset.difficulty]
            );

        }

        if (sortValue === "intermediate") {

            const score = {
                intermediate: 0,
                beginner: 1,
                advanced: 2
            };

            return (
                score[a.dataset.difficulty] -
                score[b.dataset.difficulty]
            );

        }

        return 0;

    });

    cards.forEach(card => {

        resourceGrid.appendChild(card);

    });

}

searchInput.addEventListener("input", filterResources);

typeFilter.addEventListener("change", filterResources);

difficultyFilter.addEventListener("change", filterResources);

clearSearch.addEventListener("click", () => {

    searchInput.value = "";

    filterResources();

    searchInput.focus();

});

clearFilters.addEventListener("click", () => {

    searchInput.value = "";

    typeFilter.value = "all";

    difficultyFilter.value = "all";

    filterResources();

    searchInput.focus();

});

sortFilter.addEventListener(
    "change",
    filterResources
);

filterResources();