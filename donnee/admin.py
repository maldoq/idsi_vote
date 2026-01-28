from django.contrib import admin
from .models import Electeur, Vote, Candidat, Election

# Register your models here.
admin.site.register(Electeur)
admin.site.register(Vote)
admin.site.register(Candidat)
admin.site.register(Election)
