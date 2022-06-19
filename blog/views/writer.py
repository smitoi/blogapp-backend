import datetime

from django.db.models import Count, Q
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from blog.models import Writer
from blog.serializers import WriterDetailSerializer


class WriterDashboardViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin):
    def get_queryset(self):
        queryset = Writer.objects

        if self.action == 'list':
            return queryset.annotate(
                total_articles=Count('written_articles'),
                total_recent_articles=Count(
                    'written_articles',
                    filter=Q(written_articles__created_at__gt=datetime.date.today() - datetime.timedelta(days=30))
                )
            )

        return queryset.all()

    permission_classes = [IsAuthenticated, ]
    serializer_class = WriterDetailSerializer
