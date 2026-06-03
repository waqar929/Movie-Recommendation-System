const API_URL = "http://127.0.0.1:5000/recommend";

async function getRecommendations() {
  const userId = document.getElementById("userId").value;
  const topN = document.getElementById("topN").value;
  const moviesDiv = document.getElementById("movies");
  const loader = document.getElementById("loader");

  moviesDiv.innerHTML = "";
  loader.classList.remove("hidden");

  document.getElementById("recommendations").scrollIntoView({ behavior: "smooth" });

  try {
    const response = await fetch(`${API_URL}?user_id=${userId}&top_n=${topN}`);
    const data = await response.json();

    loader.classList.add("hidden");

    if (data.error) {
      moviesDiv.innerHTML = `<div class="movie-card"><h3>Error</h3><p>${data.error}</p></div>`;
      return;
    }

    if (!data.recommendations || data.recommendations.length === 0) {
      moviesDiv.innerHTML = `<div class="movie-card"><h3>No movies found</h3><p>Try another user ID.</p></div>`;
      return;
    }

    data.recommendations.forEach((movie, index) => {
      const card = document.createElement("div");
      card.className = "movie-card";
      card.style.animationDelay = `${index * 0.08}s`;
      card.innerHTML = `
  <div class="rank">#${index + 1}</div>

  <img
    src="${movie.poster || 'https://via.placeholder.com/300x450?text=No+Poster'}"
    class="poster"
    alt="${movie.title}"
  >

  <h3>${movie.title}</h3>

  <p class="rating">
    ⭐ ${movie.rating}/5
  </p>
`;
      moviesDiv.appendChild(card);
    });
  } catch (error) {
    loader.classList.add("hidden");
    moviesDiv.innerHTML = `
      <div class="movie-card">
        <h3>Backend Not Connected</h3>
        <p>Please run your Flask backend first, then try again.</p>
      </div>
    `;
  }
}

window.addEventListener("load", () => {
  setTimeout(() => getRecommendations(), 700);
});
