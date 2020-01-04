from django.urls import path
from django.conf.urls import include
from rest_framework_nested import routers

from app.views import UserViewSet, PostViewSet, CommentViewSet, LoginView

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, base_name='users')

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', PostViewSet, base_name='posts')
posts_router = routers.NestedSimpleRouter(users_router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, base_name='comments')

urlpatterns = [
    path('login/', LoginView.as_view(), name='knox_login'),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    path('', include(posts_router.urls)),
]
