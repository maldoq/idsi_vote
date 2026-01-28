from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('electeur.urls')),
    path('dashvote/', include('dashboard.urls')),
]
