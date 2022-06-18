"""blogapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from blog.views import ArticleWriteViewSet, ArticleApproveViewSet, ArticleEditedViewSet, WriterDashboardViewSet

router = DefaultRouter()
router.register(r'article', ArticleWriteViewSet, basename='article')
router.register(r'article-approval', ArticleApproveViewSet, basename='article-approval')
router.register(r'articles-edited', ArticleEditedViewSet, basename='articles-edited')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WriterDashboardViewSet.as_view()),
    path('', include(router.urls)),
]
