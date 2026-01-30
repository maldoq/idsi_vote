from django.urls import path
from .views import login_view, qr_view, qr_view_inscription, signup_view, vote_view, logout_view


app_name = "vote"


urlpatterns = [
    path("", login_view, name="login"),
    path(
    "inscription/idsi-2026-9X3LmQ/",
    signup_view,
    name="signup"
    ),
    path("qr/", qr_view, name="qr_page"),
    path("qr-inscription/", qr_view_inscription, name="qr_page_inscription"),
    path("vote/", vote_view, name="vote"),
    path("logout/", logout_view, name="logout"),
]