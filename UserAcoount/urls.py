from django.contrib import admin
from django.urls import path, include

from .views import UserCreate

urlpatterns = [
    path(r'singup', UserCreate.as_view(), name="me.singup"),
]
