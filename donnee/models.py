from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.

GENRE_ELECTEUR = [
    ("Homme","male"),
    ("Femme","female")
]

def validate_inphb_mail(value):
    if not value.endswith('@inphb.ci'):
        raise ValidationError("Seulement le mail inphb est accepté.")
    
class Election(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    active = models.BooleanField(default=True)


    def est_ouverte(self):
        now = timezone.localtime(timezone.now())
        start = timezone.localtime(self.date_debut)
        end = timezone.localtime(self.date_fin)
        return start <= now <= end

class Electeur(AbstractUser):
    nom = models.CharField(max_length=50, blank=True)
    prenoms = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=10,choices=GENRE_ELECTEUR,null=True)
    date_naiss = models.DateField(null=True,blank=True)
    emailInst = models.CharField(max_length=50, unique=True, blank=False,null=False, validators=[validate_inphb_mail])
    telephone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Le numéro de téléphone doit etre dans le format : +225xxxxxxxxxx"
        )]
    )
    est_eligible_vote = models.BooleanField(default=True,blank=False)
    a_vote = models.BooleanField(default=False,blank=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "emailInst"
    REQUIRED_FIELDS = ["emailInst","telephone"]

class Candidat(models.Model):
    nom_complet = models.CharField(max_length=200)

    filiere = models.CharField(
    max_length=75,
    null=True,
    blank=True
    )

    election = models.ForeignKey(
    Election,
    on_delete=models.CASCADE
    )

    photo = models.ImageField(
    upload_to="candidat/",
    null=True,
    blank=True
    )

    def total_votes(self):
        return Vote.objects.filter(candidat=self).count()

    def __str__(self):
        return self.nom_complet

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=None)
    candidat = models.ForeignKey(Candidat,on_delete=models.DO_NOTHING)
    electeur = models.ForeignKey(Electeur,on_delete=models.DO_NOTHING)
    date_vote = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('election', 'electeur')
