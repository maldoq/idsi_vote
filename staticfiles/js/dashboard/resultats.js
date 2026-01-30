// ===========================
// DONNÉES FICTIVES - RÉSULTATS FINAUX
// ===========================

const finalResults = [
    { id: 1, name: "Marie Dubois", votes: 2847 },
    { id: 2, name: "Jean Martin", votes: 2135 },
    { id: 3, name: "Sophie Bernard", votes: 1654 },
    { id: 4, name: "Pierre Lefebvre", votes: 982 },
    { id: 5, name: "Claire Moreau", votes: 756 }
];

const TOTAL_ELECTEURS = 10000;
const CLOSURE_DATE = "28 Janvier 2026";

// ===========================
// FONCTIONS UTILITAIRES
// ===========================

function calculateTotalVotes() {
    return finalResults.reduce((sum, candidate) => sum + candidate.votes, 0);
}

function calculatePercentage(votes, total) {
    if (total === 0) return 0;
    return ((votes / total) * 100).toFixed(1);
}

// ===========================
// MISE À JOUR DES STATISTIQUES
// ===========================

function updateGlobalStats() {
    const totalVotes = calculateTotalVotes();
    const participationRate = ((totalVotes / TOTAL_ELECTEURS) * 100).toFixed(1);
    const validVotes = totalVotes; // Dans cet exemple, tous les votes sont valides
    
    document.getElementById('totalVotesResult').textContent = totalVotes.toLocaleString('fr-FR');
    document.getElementById('participationRateResult').textContent = participationRate + '%';
    document.getElementById('validVotesResult').textContent = validVotes.toLocaleString('fr-FR');
    document.getElementById('closureDate').textContent = CLOSURE_DATE;
}

// ===========================
// GÉNÉRATION DU CLASSEMENT
// ===========================

function renderResults() {
    const resultsContainer = document.getElementById('resultsList');
    resultsContainer.innerHTML = '';
    
    const totalVotes = calculateTotalVotes();
    
    // Trier par nombre de votes (ordre décroissant)
    const sortedResults = [...finalResults].sort((a, b) => b.votes - a.votes);
    
    sortedResults.forEach((candidate, index) => {
        const position = index + 1;
        const percentage = calculatePercentage(candidate.votes, totalVotes);
        
        // Créer la carte de résultat
        const card = document.createElement('div');
        card.className = 'result-card';
        
        // Carte spéciale pour le vainqueur (1er)
        if (position === 1) {
            card.classList.add('winner');
            
            // Badge vainqueur
            const badge = document.createElement('div');
            badge.className = 'winner-badge';
            badge.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 9H4.5a2.5 2.5 0 010-5H6"/>
                    <path d="M18 9h1.5a2.5 2.5 0 000-5H18"/>
                    <path d="M4 22h16"/>
                    <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
                    <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
                    <path d="M18 2H6v7a6 6 0 0012 0V2z"/>
                </svg>
                <span>Vainqueur</span>
            `;
            card.appendChild(badge);
        }
        
        // Position
        const positionDiv = document.createElement('div');
        positionDiv.className = 'result-position';
        positionDiv.textContent = position;
        
        // Info candidat
        const info = document.createElement('div');
        info.className = 'result-info';
        
        const name = document.createElement('div');
        name.className = 'result-name';
        name.textContent = candidate.name;
        
        const votes = document.createElement('div');
        votes.className = 'result-votes';
        votes.innerHTML = `<span class="result-votes-count">${candidate.votes.toLocaleString('fr-FR')}</span> votes`;
        
        info.appendChild(name);
        info.appendChild(votes);
        
        // Métriques (pourcentage + barre)
        const metrics = document.createElement('div');
        metrics.className = 'result-metrics';
        
        const percentageDiv = document.createElement('div');
        percentageDiv.className = 'result-percentage';
        percentageDiv.textContent = percentage + '%';
        
        const bar = document.createElement('div');
        bar.className = 'result-bar';
        
        const barFill = document.createElement('div');
        barFill.className = 'result-bar-fill';
        barFill.style.width = '0%'; // Commencer à 0 pour l'animation
        
        bar.appendChild(barFill);
        
        metrics.appendChild(percentageDiv);
        metrics.appendChild(bar);
        
        // Assembler la carte
        card.appendChild(positionDiv);
        card.appendChild(info);
        card.appendChild(metrics);
        
        resultsContainer.appendChild(card);
        
        // Animer la barre de progression après un court délai
        setTimeout(() => {
            barFill.style.width = percentage + '%';
        }, 100 + (index * 100)); // Délai progressif pour effet cascade
    });
}

// ===========================
// INITIALISATION
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    updateGlobalStats();
    renderResults();
});

// ===========================
// GESTION DE LA DÉCONNEXION
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    const logoutLink = document.querySelector('.logout');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                window.location.href = 'login.html';
            }
        });
    }
});