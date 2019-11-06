from django.conf import settings
from django.conf.urls import include, url
from rest_framework import routers
from rest_framework.authtoken import views
from app.views import user

router = routers.DefaultRouter()
router.register(r'users', user.UserViewSet, base_name='users')

urlpatterns = [
    url(r'^login/', views.obtain_auth_token),
] + router.urls
