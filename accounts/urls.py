from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuthorizationView.as_view(), name="Authorization"),
    path("profile/", views.ProfileView.as_view(), name="Profile"),
    path("logout/", views.LogoutView.as_view(), name="Logout")
]