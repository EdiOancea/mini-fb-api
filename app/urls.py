from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken import views
from app.views.user import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    url(r'^login/', views.obtain_auth_token),
] + router.urls
