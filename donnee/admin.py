from django.contrib import admin
from .models import Electeur, Vote, Candidat

# Register your models here.
admin.site.register(Electeur)
admin.site.register(Vote)
admin.site.register(Candidat)
