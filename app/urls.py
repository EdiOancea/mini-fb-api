from django.urls import path
from django.conf.urls import include
from rest_framework_nested import routers

from app.views import UserViewSet, PostViewSet, LoginView

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, base_name='users')

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', PostViewSet, base_name='posts')

urlpatterns = [
    path('login/', LoginView.as_view(), name='knox_login'),
    path('', include(router.urls)),
    path('', include(users_router.urls))
]
