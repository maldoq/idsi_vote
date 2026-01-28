from django.urls import reverse
import qrcode
import io
import base64
from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from donnee.models import Electeur, Election, Candidat, Vote

# Create your views here.
def qr_view(request):
    # Les URLs de redirection
    login_url = request.build_absolute_uri(reverse("vote:login"))


    # Fonction pour générer un QR code en base64
    def make_qr(url):
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{qr_b64}"


    context = {
    "qr_login_url": make_qr(login_url),
    }
    return render(request, "electeur/qr_redirect.html", context)

def qr_view_inscription(request):
    # Les URLs de redirection
    signup_url = request.build_absolute_uri(reverse("vote:signup"))


    # Fonction pour générer un QR code en base64
    def make_qr(url):
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{qr_b64}"


    context = {
    "qr_signup_url": make_qr(signup_url),
    }
    return render(request, "electeur/qr_redirect_inscription.html", context)

@csrf_protect
def login_view(request):
    error = None


    # 1️⃣ Vérifier s’il y a une élection active
    try:
        election = Election.objects.get(active=True)
    except Election.DoesNotExist:
        error = "Aucune élection active pour le moment."
        return render(request, "electeur/login.html", {"error": error})
    except Election.MultipleObjectsReturned:
        error = "Erreur système : plusieurs élections actives."
        return render(request, "electeur/login.html", {"error": error})


    # 2️⃣ Vérifier si l’élection est ouverte
    if not election.est_ouverte():
        error = "Le vote n'est pas ouvert. Veuillez respecter la période électorale."
        return render(request, "electeur/login.html", {"error": error})


    # 3️⃣ Traitement du formulaire
    if request.method == "POST":
        email = request.POST.get("email")
        tel = request.POST.get("tel")
        password = request.POST.get("password")


        if not email or not tel or not password:
            error = "Tous les champs sont obligatoires."
            return render(request, "electeur/login.html", {"error": error})


        telephone = "+225" + tel


        try:
            electeur = Electeur.objects.get(
            emailInst=email,
            telephone=telephone
            )
        except Electeur.DoesNotExist:
            error = "Identifiants ou mot de passe incorrects."
            return render(request, "electeur/login.html", {"error": error})


        user = authenticate(
        request,
        username=electeur.username,
        password=password
        )


        if user is None:
            error = "Identifiants ou mot de passe incorrects."
            return render(request, "electeur/login.html", {"error": error})


        if not user.est_eligible_vote:
            error = "Vous n'êtes pas autorisé à voter."
            return render(request, "electeur/login.html", {"error": error})


        # 4️⃣ Connexion OK
        login(request, user)
        return redirect("vote:vote")


    return render(request, "electeur/login.html")

def signup_view(request):
    now = timezone.now()


    # ⛔ Blocage hors période d'inscription
    if now < settings.INSCRIPTION_START or now > settings.INSCRIPTION_END:
        raise Http404()


    if request.method == "POST":
        nom = request.POST.get("nom")
        prenoms = request.POST.get("prenoms")
        genre = request.POST.get("genre")
        date_naiss = request.POST.get("date_naiss")
        telephone = request.POST.get("telephone")
        email = request.POST.get("emailInst")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        tel = "+225" + telephone


        # 1️⃣ Vérifications de base
        if not all([nom, prenoms, genre, date_naiss, tel, email, pass1, pass2]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, "electeur/signup.html")


        if pass1 != pass2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "electeur/signup.html")


        if not email.endswith("@inphb.ci"):
            messages.error(request, "Seuls les emails institutionnels INPHB sont acceptés.")
            return render(request, "electeur/signup.html")


        # 2️⃣ Unicité
        if Electeur.objects.filter(emailInst=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "electeur/signup.html")


        if Electeur.objects.filter(telephone=tel).exists():
            messages.error(request, "Ce numéro est déjà utilisé.")
            return render(request, "electeur/signup.html")


        # 3️⃣ Création utilisateur (PROPRE)
        user = Electeur.objects.create_user(
        username=email.split("@")[0], # simple et stable
        emailInst=email,
        password=pass1
        )


        user.nom = nom
        user.prenoms = prenoms
        user.genre = genre
        user.date_naiss = date_naiss
        user.telephone = tel
        user.is_active = True
        user.save()


        messages.success(request, "Inscription réussie. Vous pouvez vous connecter.")
        return redirect("vote:login")


    return render(request, "electeur/signup.html")

@login_required(login_url="vote:login")
def vote_view(request):
    now = timezone.now()


    # 1️⃣ Récupérer l'élection active
    election = Election.objects.filter(
    date_debut__lte=now,
    date_fin__gte=now,
    active=True
    ).first()


    if not election:
        messages.error(
        request,
        "Aucune élection n'est en cours actuellement."
        )
        return redirect("vote:login")


    # 2️⃣ Vérifier si l'utilisateur a déjà voté
    already_voted = Vote.objects.filter(
    electeur=request.user,
    election=election
    ).exists()


    if already_voted:
        messages.warning(
        request,
        "Vous avez déjà voté. Merci pour votre participation."
        )
        return render(
        request,
        "electeur/vote_done.html", # page simple "vote terminé"
        {"election": election}
        )


    # 3️⃣ Traitement du vote
    if request.method == "POST":
        candidat_id = request.POST.get("candidat_id")


        candidat = get_object_or_404(
        Candidat,
        id=candidat_id,
        election=election
        )


        # Sécurité ultime : empêcher double vote
        Vote.objects.create(
        electeur=request.user,
        candidat=candidat,
        election=election
        )


        messages.success(
        request,
        "Votre vote a été enregistré avec succès."
        )


        return redirect("vote:vote") # recharge → bloqué ensuite


    # 4️⃣ Affichage des candidats
    candidats = Candidat.objects.filter(
    election=election
    )


    context = {
    "election": election,
    "candidats": candidats,
    }


    return render(request, "electeur/vote_page.html", context)

@login_required
def logout_view(request):
    """
    Déconnecte l'utilisateur et redirige vers la page de login.
    """
    auth_logout(request)
    return redirect("vote:login")
