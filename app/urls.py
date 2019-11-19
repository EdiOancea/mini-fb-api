from django.urls import path
from rest_framework import routers

from app.views.user import UserViewSet
from app.views.auth import LoginView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    path('login/', LoginView.as_view(), name='knox_login'),
] + router.urls
