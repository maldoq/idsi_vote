from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth import logout
from django.db.models import Count

from donnee.models import Election, Candidat, Vote, Electeur


@staff_member_required(login_url="vote:login")
def dashboard_view(request):
    # 1️⃣ Élection active
    election = Election.objects.filter(active=True).first()

    if not election:
        return render(request, "dashboard/dashboard.html", {
            "election_name": "Aucune élection active",
            "election_open": False,
            "total_votes": 0,
            "total_candidates": 0,
            "participation_rate": 0,
            "leading_candidate": None,
            "top_candidates": [],
        })

    # 2️⃣ Tous les candidats + nombre de votes
    candidats = (
        Candidat.objects
        .filter(election=election)
        .annotate(votes_count=Count("vote"))
        .order_by("-votes_count")
    )

    total_votes = sum(c.votes_count for c in candidats)
    total_candidates = candidats.count()

    # 3️⃣ Leader actuel
    leader = candidats.first()
    leading_candidate = leader.nom_complet if leader else None

    # 4️⃣ Top 3
    top_candidates = [
        {
            "name": c.nom_complet,
            "votes": c.votes_count
        }
        for c in candidats[:3]
    ]

    # Total des électeurs enregistrés
    total_electeurs = Electeur.objects.all().count()

    # Taux de participation basé sur le total des électeurs
    participation_rate = round((total_votes / total_electeurs) * 100, 2) if total_electeurs > 0 else 0

    context = {
        "election_name": election.titre,
        "election_open": election.est_ouverte(),

        "total_votes": total_votes,
        "total_candidates": total_candidates,
        "total_electeurs": total_electeurs,
        "participation_rate": participation_rate,

        "leading_candidate": leading_candidate,
        "top_candidates": top_candidates,
    }

    return render(request, "dashboard/dashboard.html", context)

@staff_member_required(login_url="vote:login")
def election_settings_view(request):
    election = Election.objects.filter(active=True).first()

    if not election:
        return render(request, "dashboard/election_settings.html", {
            "election": None,
            "election_open": False,
            "total_votes": 0,
            "leader": None,
            "participation_rate": 0,
            "last_vote_time": None,
        })

    candidats = (
        Candidat.objects
        .filter(election=election)
        .annotate(votes_count=Count("vote"))
        .order_by("-votes_count")
    )

    total_votes = sum(c.votes_count for c in candidats)

    leader = candidats.first().nom_complet if candidats.exists() else None

    last_vote = (
        Vote.objects
        .filter(candidat__election=election)
        .order_by("-date_vote")
        .first()
    )

    # Total des électeurs enregistrés
    total_electeurs = Vote.objects.filter(candidat__election=election).values('electeur').distinct().count()

    # Taux de participation basé sur le total des électeurs
    participation_rate = round((total_votes / total_electeurs) * 100, 2) if total_electeurs > 0 else 0

    print(election.est_ouverte())
    context = {
        "election": election,
        "election_open": election.est_ouverte(),
        "total_votes": total_votes,
        "leader": leader,
        "participation_rate": participation_rate,
        "last_vote_time": last_vote.date_vote if last_vote else None,
    }

    return render(request, "dashboard/election_settings.html", context)

@staff_member_required(login_url="vote:login")
def resultats_view(request):
    election = Election.objects.filter(active=True).first()

    if not election:
        return render(request, "dashboard/resultats.html", {
            "finalResults": [],
            "election": None,
            "election_open": False,
            "total_votes": 0,
            "valid_votes": 0,
            "participation_rate": 0,
            "candidats": [],
        })

    candidats = (
        Candidat.objects
        .filter(election=election)
        .annotate(votes_count=Count("vote"))
        .order_by("-votes_count")
    )

    total_votes = sum(c.votes_count for c in candidats)
    valid_votes = total_votes  # si tu veux filtrer les votes invalides, on peut ajouter un flag dans Vote

    # Total des électeurs enregistrés
    total_electeurs = Electeur.objects.all().count()

    # Taux de participation basé sur le total des électeurs
    participation_rate = round((total_votes / total_electeurs) * 100, 2) if total_electeurs > 0 else 0

    # Construction du tableau finalResults pour le JS
    finalResults = [
        {
            "id": c.id,
            "name": c.nom_complet,
            "votes": c.votes_count
        }
        for c in candidats
    ]

    context = {
        "finalResults": finalResults,
        "election": election,
        "election_open": election.est_ouverte(),
        "total_electeurs": total_electeurs,
        "total_votes": total_votes,
        "valid_votes": valid_votes,
        "participation_rate": participation_rate,
        "candidats": candidats,
    }

    return render(request, "dashboard/resultats.html", context)

@require_POST
@staff_member_required(login_url="vote:login")
def update_election_info(request):
    election = Election.objects.first()  # une seule élection

    election.titre = request.POST.get("titre")
    election.description = request.POST.get("description")

    date_debut = parse_datetime(request.POST.get("date_debut"))
    date_fin = parse_datetime(request.POST.get("date_fin"))

    if not date_debut or not date_fin:
        return JsonResponse({"error": "Dates invalides"}, status=400)

    if date_debut >= date_fin:
        return JsonResponse({"error": "La date de fin doit être après la date de début"}, status=400)

    election.date_debut = date_debut
    election.date_fin = date_fin
    election.save()

    return JsonResponse({"success": True})

@staff_member_required(login_url="vote:login")
def logout_view(request):
    logout(request)  # Supprime la session de l'utilisateur
    return redirect('vote:login')  # Redirige vers la page de connexion
