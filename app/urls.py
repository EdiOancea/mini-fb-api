from django.conf import settings
from rest_framework import routers

from app.views import user

router = routers.DefaultRouter()
router.register(r'users', user.UserViewSet)

urlpatterns = router.urls
