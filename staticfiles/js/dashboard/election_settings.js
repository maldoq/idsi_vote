// ===========================
// GESTION DE L'ÉTAT
// ===========================

function updateElectionStatus(newStatus) {
    electionState.status = newStatus;
    
    // Mise à jour du badge de statut
    const statusBadge = document.getElementById('currentStatusBadge');
    const statusDot = statusBadge.querySelector('.status-dot');
    const statusText = statusBadge.querySelector('.status-badge-text');
    
    // Retirer toutes les classes de statut
    statusBadge.classList.remove('badge-open', 'badge-closed', 'badge-pending');
    statusDot.classList.remove('status-open', 'status-closed', 'status-pending');
    
    // Appliquer les nouvelles classes
    switch(newStatus) {
        case 'open':
            statusBadge.classList.add('badge-open');
            statusDot.classList.add('status-open');
            statusText.textContent = 'Ouverte';
            updateNavStatus('Élection ouverte', 'status-open');
            break;
        case 'closed':
            statusBadge.classList.add('badge-closed');
            statusDot.classList.add('status-closed');
            statusText.textContent = 'Clôturée';
            updateNavStatus('Élection clôturée', 'status-closed');
            break;
        case 'pending':
            statusBadge.classList.add('badge-pending');
            statusDot.classList.add('status-pending');
            statusText.textContent = 'Suspendue';
            updateNavStatus('Élection suspendue', 'status-pending');
            break;
    }
}

function updateNavStatus(text, statusClass) {
    const navStatus = document.getElementById('navStatus');
    const navIndicator = document.querySelector('.election-status .status-indicator');
    
    navStatus.textContent = text;
    navIndicator.classList.remove('status-open', 'status-closed', 'status-pending');
    navIndicator.classList.add(statusClass);
}

// ===========================
// MISE À JOUR DES STATISTIQUES
// ===========================

function updateStats() {
    if (!electionData.lastVoteTime) return;

    const lastVote = new Date(electionData.lastVoteTime);
    const participationRate = ((electionData.totalVotes / TOTAL_ELECTEURS) * 100).toFixed(1);
    const timeSinceLastVote = getTimeSinceLastVote();

    document.getElementById('statsVotes').textContent = electionData.totalVotes.toLocaleString('fr-FR');
    document.getElementById('statsLeader').textContent = electionData.leadingCandidate || '--';
    document.getElementById('statsLastVote').textContent = timeSinceLastVote;
    document.getElementById('statsParticipation').textContent = participationRate + '%';

    function getTimeSinceLastVote() {
        const now = new Date();
        const diff = Math.floor((now - lastVote) / 1000);

        if (diff < 60) return `Il y a ${diff} secondes`;
        if (diff < 3600) return `Il y a ${Math.floor(diff / 60)} minute${Math.floor(diff / 60) > 1 ? 's' : ''}`;
        return `Il y a ${Math.floor(diff / 3600)} heure${Math.floor(diff / 3600) > 1 ? 's' : ''}`;
    }
}

function getTimeSinceLastVote() {
    const now = new Date();
    const diff = Math.floor((now - electionState.lastVoteTime) / 1000); // en secondes
    
    if (diff < 60) {
        return `Il y a ${diff} secondes`;
    } else if (diff < 3600) {
        const minutes = Math.floor(diff / 60);
        return `Il y a ${minutes} minute${minutes > 1 ? 's' : ''}`;
    } else {
        const hours = Math.floor(diff / 3600);
        return `Il y a ${hours} heure${hours > 1 ? 's' : ''}`;
    }
}

// ===========================
// GESTION DES MODALS
// ===========================

let currentAction = null;

function showModal(title, message, onConfirm) {
    const modal = document.getElementById('confirmModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    modal.classList.add('active');
    
    currentAction = onConfirm;
}

function hideModal() {
    const modal = document.getElementById('confirmModal');
    modal.classList.remove('active');
    currentAction = null;
}

// ===========================
// GESTION DES TOASTS
// ===========================

function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    toast.classList.add('active');
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// ===========================
// ACTIONS DE BOUTONS
// ===========================

function activateElection() {
    showModal(
        'Activer l\'élection',
        'Êtes-vous sûr de vouloir activer l\'élection ? Les électeurs pourront commencer à voter.',
        () => {
            updateElectionStatus('open');
            showToast('L\'élection a été activée avec succès');
            hideModal();
        }
    );
}

function suspendElection() {
    showModal(
        'Suspendre l\'élection',
        'Êtes-vous sûr de vouloir suspendre l\'élection ? Le vote sera temporairement interrompu.',
        () => {
            updateElectionStatus('pending');
            showToast('L\'élection a été suspendue');
            hideModal();
        }
    );
}

function closeElection() {
    showModal(
        'Clôturer l\'élection',
        'Êtes-vous sûr de vouloir clôturer l\'élection ? Cette action est irréversible et empêchera tout nouveau vote.',
        () => {
            updateElectionStatus('closed');
            showToast('L\'élection a été clôturée définitivement');
            hideModal();
        }
    );
}

function saveElectionInfo() {
    const title = document.getElementById('electionTitle').value;
    const description = document.getElementById('electionDescription').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    if (!title || !description || !startDate || !endDate) {
        alert('Veuillez remplir tous les champs obligatoires');
        return;
    }
    
    showToast('Les informations ont été enregistrées avec succès');
}

function lockResults() {
    if (electionState.isLocked) {
        alert('Les résultats sont déjà verrouillés');
        return;
    }
    
    showModal(
        'Verrouiller les résultats',
        'ATTENTION : Cette action est irréversible ! Le verrouillage rendra les résultats définitifs et empêchera toute modification ultérieure. Voulez-vous continuer ?',
        () => {
            electionState.isLocked = true;
            updateElectionStatus('closed');
            
            // Désactiver le bouton
            const lockBtn = document.getElementById('lockResultsBtn');
            lockBtn.disabled = true;
            lockBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>
                <span>Résultats verrouillés</span>
            `;
            
            showToast('Les résultats ont été verrouillés de manière définitive');
            hideModal();
        }
    );
}

// ===========================
// EVENT LISTENERS
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    // Initialisation
    updateElectionStatus('open');
    updateStats();
    
    // Simulation de nouveaux votes (toutes les 5 secondes)
    setInterval(simulateNewVote, 5000);
    
    // Mise à jour de l'affichage du temps (toutes les secondes)
    setInterval(updateStats, 1000);
    
    // Boutons d'état
    document.getElementById('activateBtn').addEventListener('click', activateElection);
    document.getElementById('suspendBtn').addEventListener('click', suspendElection);
    document.getElementById('closeBtn').addEventListener('click', closeElection);
    
    // Bouton de sauvegarde
    document.getElementById('saveInfoBtn').addEventListener('click', saveElectionInfo);
    
    // Bouton de verrouillage
    document.getElementById('lockResultsBtn').addEventListener('click', lockResults);
    
    // Modal
    document.getElementById('modalClose').addEventListener('click', hideModal);
    document.getElementById('modalCancel').addEventListener('click', hideModal);
    document.getElementById('modalConfirm').addEventListener('click', () => {
        if (currentAction) {
            currentAction();
        }
    });
    
    // Fermer la modal en cliquant en dehors
    document.getElementById('confirmModal').addEventListener('click', (e) => {
        if (e.target.id === 'confirmModal') {
            hideModal();
        }
    });
    
    // Déconnexion
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

// ===========================
// GESTION DES RACCOURCIS CLAVIER
// ===========================

document.addEventListener('keydown', (e) => {
    // Échap pour fermer la modal
    if (e.key === 'Escape') {
        hideModal();
    }
    
    // Entrée pour confirmer dans la modal
    if (e.key === 'Enter' && document.getElementById('confirmModal').classList.contains('active')) {
        if (currentAction) {
            currentAction();
        }
    }
});