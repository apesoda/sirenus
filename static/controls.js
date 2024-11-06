//Play requested sound
function playSound(soundFile) {
    fetch('/play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'sound_file': soundFile }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
//Kill sound playing
function stopSound() {
    fetch('/stop', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
let currentPage = 1;
let totalPages = 1;  // This will be updated dynamically

async function fetchSounds(page) {
    try {
        const response = await fetch(`/sounds?page=${page}`);
        const data = await response.json();

        if (response.ok) {
            updateSounds(data.sounds);
            updatePagination(data.page, data.total_pages);
        } else {
            console.error("Error fetching sounds:", data.message);
        }
    } catch (error) {
        console.error("Error fetching sounds:", error);
    }
}

function updateSounds(sounds) {
    const buttonContainer = document.getElementById("button-container");
    buttonContainer.innerHTML = '';  // Clear existing buttons

    sounds.forEach(sound => {
        const button = document.createElement("button");
        button.textContent = sound.replace(".mp3", "").replace("_", " ");
        button.onclick = () => playSound(sound);
        buttonContainer.appendChild(button);
        buttonContainer.appendChild(document.createElement("br"));
    });
}

function updatePagination(page, total) {
    currentPage = page;
    totalPages = total;

    document.getElementById("page-info").textContent = `Page ${page} of ${total}`;
    document.getElementById("prev-button").disabled = page <= 1;
    document.getElementById("next-button").disabled = page >= total;
}

function changePage(direction) {
    const newPage = currentPage + direction;
    if (newPage >= 1 && newPage <= totalPages) {
        fetchSounds(newPage);
    }
}

// Initial fetch to load the first page
document.addEventListener("DOMContentLoaded", () => {
    fetchSounds(currentPage);
});

