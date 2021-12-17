from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:shorten_url>/", views.redirect_url, name="redirect"),
]
