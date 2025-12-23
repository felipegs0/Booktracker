const modal = document.querySelector("#modal")

function openModal(button)
{
    document.getElementById("modal_google_id").value = button.dataset.googleId;
    document.getElementById("modal_title").value = button.dataset.title;
    document.getElementById("modal_authors").value = button.dataset.authors;
    document.getElementById("modal_thumbnail").value = button.dataset.thumbnail;
    document.getElementById("modal_description").value = button.dataset.description;

    modal.classList.remove("hidden")
}

function closeModal() 
{
    modal.classList.add("hidden")
}
