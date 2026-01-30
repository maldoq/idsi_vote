from django.urls import path

from .views import dashboard_view, election_settings_view, resultats_view, logout_view, update_election_info

app_name = "dashboard"

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("settings/", election_settings_view, name="election_settings"),
    path("resultats/", resultats_view, name="resultats"),
    path("logout/", logout_view, name="logout"),
    path("election/update/", update_election_info, name="update_election_info"),
]
