from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'ayurtp'

urlpatterns = [
    #=============================================== Homepage Paths ===================================================================
    path("", views.index, name = "index"), #Homepage   
    path("Ayurvedic-Therapeutics/search", views.search, name = "search"),
    path("Ayurvedic-Therapeutics/download", views.download, name = "download"),
    path("Ayurvedic-Therapeutics/statistics", views.statistics, name = "statistics"),
    path("Ayurvedic-Therapeutics/help", views.help, name = "help"),
]
