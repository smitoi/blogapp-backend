from rest_framework import viewsets

from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article
from blog.permissions import IsEditor
from blog.serializers import ArticleWriterSerializer, ArticleApprovalSerializer
from django.db.models import Q


class ArticleWriteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleWriterSerializer
    ordering = ('-created_at',)

    def perform_create(self, serializer):
        serializer.save(written_by=self.request.user.writer_profile)


class ArticleApproveViewSet(LoginRequiredMixin,
                            viewsets.GenericViewSet,
                            viewsets.mixins.ListModelMixin,
                            viewsets.mixins.UpdateModelMixin):
    permission_classes = [IsEditor]
    queryset = Article.objects.filter(status=Article.ArticleStatus.DRAFT)
    serializer_class = ArticleApprovalSerializer
    ordering = ('-created_at',)


class ArticleEditedViewSet(LoginRequiredMixin,
                           viewsets.GenericViewSet,
                           viewsets.mixins.ListModelMixin):
    permission_classes = [IsEditor]
    queryset = Article.objects.filter(~Q(status=Article.ArticleStatus.DRAFT))
    serializer_class = ArticleApprovalSerializer
    ordering = ('-created_at',)
