from django.urls import path
from authapp.views import *

urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),
    path('csrf', GetCsrfTokenView.as_view(), name='csrf_token'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
