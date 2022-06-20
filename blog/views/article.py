from rest_framework import viewsets, mixins

from rest_framework.permissions import IsAuthenticated

from blog.models import Article
from blog.permissions import IsEditor, IsWriter
from blog.serializers import ArticleWriterSerializer, ArticleApprovalSerializer
from django.db.models import Q


class ArticleWriteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsWriter, ]
    queryset = Article.objects.all()
    serializer_class = ArticleWriterSerializer
    ordering = ('-created_at',)

    def get_queryset(self):
        if self.action == 'update':
            return Article.objects.filter(~Q(status=Article.ArticleStatus.APPROVED)).all()

        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(written_by=self.request.user.writer_profile)

    def perform_update(self, serializer):
        serializer.save(status=Article.ArticleStatus.DRAFT)


class ArticleApproveViewSet(mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsEditor, ]
    queryset = Article.objects.filter(status=Article.ArticleStatus.DRAFT)
    serializer_class = ArticleApprovalSerializer
    ordering = ('-created_at',)

    def perform_update(self, serializer):
        serializer.save(edited_by=self.request.user.writer_profile)


class ArticleEditedViewSet(viewsets.GenericViewSet,
                           viewsets.mixins.ListModelMixin):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ArticleApprovalSerializer
    ordering = ('-created_at',)

    def get_queryset(self):
        return Article.objects.filter(~Q(status=Article.ArticleStatus.DRAFT), edited_by=self.request.user.id)
