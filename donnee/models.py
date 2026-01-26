from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

import random

# Create your models here.

def validate_inphb_mail(value):
    if not value.endswith('@inphb.ci'):
        raise ValidationError("Seulement le mail inphb est accepté.")

class Electeur(AbstractUser):
    nom = models.CharField(max_length=50, blank=True)
    prenoms = models.CharField(max_length=100, blank=True)
    emailInst = models.CharField(max_length=50, unique=True, blank=False,null=False, validators=[validate_inphb_mail])
    telephone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Le numéro de téléphone doit etre dans le format : +225xxxxxxxxxx"
        )]
    )
    est_eligible_vote = models.BooleanField()
    a_vote = models.BooleanField()

    EMAIL_FIELD = "emailInst"
    REQUIRED_FIELDS = ["emailInst","telephone"]

class Candidat(models.Model):
    nom_complet = models.CharField()
    photo = models.ImageField(upload_to="/static/candidat/")

class Vote(models.Model):
    id = models.CharField(primary_key=True, unique=True)
    candidat = models.ForeignKey(Candidat,on_delete=models.DO_NOTHING)
    electeur = models.ForeignKey(Electeur,on_delete=models.DO_NOTHING)
    date_vote = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        rand_num = str(random.randint(1000000,9999999))
        date_now = str(timezone.now())
        self.id = rand_num + date_now
        return super().save()