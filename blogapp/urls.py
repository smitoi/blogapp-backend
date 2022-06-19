from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from blog.views import ArticleWriteViewSet, ArticleApproveViewSet, ArticleEditedViewSet, WriterDashboardViewSet

router = DefaultRouter()
router.register(r'article', ArticleWriteViewSet, basename='article-writer')
router.register(r'writer', WriterDashboardViewSet, basename='writer')
router.register(r'article-approval', ArticleApproveViewSet, basename='article-approval')
router.register(r'articles-edited', ArticleEditedViewSet, basename='articles-edited')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/token/obtain/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
]
