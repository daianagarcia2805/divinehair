from django.urls import path
from .views import home_view, contato_view

app_name = "core"

urlpatterns = [
    path("", home_view, name="main"),
    path("contato/", contato_view, name="contato"),
]