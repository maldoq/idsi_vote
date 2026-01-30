import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "idsi_vote.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@inphb.com")
ADMIN_TEL = os.environ.get("ADMIN_TEL", "+2250101010101")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "adminadmin")

if not User.objects.filter(username=ADMIN_USERNAME).exists():
    User.objects.create_superuser(
        username=ADMIN_USERNAME,
        emailInst=ADMIN_EMAIL,
        telephone=ADMIN_TEL,
        password=ADMIN_PASSWORD
    )
    print(f"Superuser {ADMIN_USERNAME} créé avec succès !")
else:
    print(f"Superuser {ADMIN_USERNAME} existe déjà.")
