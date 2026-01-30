/* ===============================
   DONNÉES GLOBALES (Django)
================================ */

// Injectées depuis le template
// const candidatesData = [{name, votes}];
// const TOTAL_ELECTEURS = 120;

let candidates = candidatesData || [];

/* ===============================
   OUTILS
================================ */

function getTotalVotes() {
    return candidates.reduce((sum, c) => sum + c.votes, 0);
}

function getParticipationRate() {
    if (TOTAL_ELECTEURS === 0) return 0;
    return ((getTotalVotes() / TOTAL_ELECTEURS) * 100).toFixed(2);
}

function getLeadingCandidate() {
    if (!candidates.length) return "--";
    return [...candidates].sort((a, b) => b.votes - a.votes)[0].name;
}

/* ===============================
   DASHBOARD
================================ */

function updateDashboard() {
    document.getElementById("totalVotes").textContent = getTotalVotes();
    document.getElementById("participationRate").textContent =
        getParticipationRate() + "%";
    document.getElementById("leadingCandidate").textContent =
        getLeadingCandidate();
    document.getElementById("lastUpdate").textContent =
        new Date().toLocaleTimeString("fr-FR");
}

/* ===============================
   HISTOGRAMME
================================ */

function renderChart() {
    const chart = document.getElementById("votesChart");
    chart.innerHTML = "";

    if (!candidates.length) {
        chart.innerHTML = "<p>Aucun vote enregistré</p>";
        return;
    }

    const maxVotes = Math.max(...candidates.map(c => c.votes), 1);

    candidates.forEach(c => {
        const bar = document.createElement("div");
        bar.className = "chart-bar";

        const value = document.createElement("div");
        value.className = "bar-value";
        value.textContent = c.votes;

        const fillContainer = document.createElement("div");
        fillContainer.className = "bar-fill-container";

        const fill = document.createElement("div");
        fill.className = "bar-fill";
        fill.style.height = (c.votes / maxVotes * 100) + "%";

        const label = document.createElement("div");
        label.className = "bar-label";
        label.textContent = c.name;

        fillContainer.appendChild(fill);
        bar.appendChild(value);
        bar.appendChild(fillContainer);
        bar.appendChild(label);

        chart.appendChild(bar);
    });
}

/* ===============================
   TOP 3
================================ */

function renderTopCandidates() {
    const container = document.getElementById("topCandidates");
    container.innerHTML = "";

    const sorted = [...candidates].sort((a, b) => b.votes - a.votes).slice(0, 3);

    sorted.forEach((c, index) => {
        const div = document.createElement("div");
        div.className = "ranking-item";
        div.innerHTML = `
            <span class="rank">${index + 1}</span>
            <span class="name">${c.name}</span>
            <span class="votes">${c.votes} votes</span>
        `;
        container.appendChild(div);
    });
}

/* ===============================
   WEBSOCKET
================================ */

const socket = new WebSocket(
    "ws://" + window.location.host + "/ws/dashboard/"
);

socket.onopen = () => {
    console.log("✅ WebSocket dashboard connecté");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "votes_update") {
        // Format attendu :
        // data.candidats = [{name, votes}]
        candidates = data.candidats;

        updateDashboard();
        renderChart();
        renderTopCandidates();
    }
};

socket.onclose = () => {
    console.warn("❌ WebSocket dashboard fermé");
};

/* ===============================
   INITIALISATION
================================ */

document.addEventListener("DOMContentLoaded", () => {
    updateDashboard();
    renderChart();
    renderTopCandidates();
});