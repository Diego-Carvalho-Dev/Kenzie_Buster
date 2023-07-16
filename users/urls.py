from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/login/", views.LoginView.as_view()),
    path("users/<int:user_id>/", views.UserDetailView.as_view()),
]
