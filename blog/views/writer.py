import datetime

from django.db.models import Count, Q
from rest_framework import generics

from blog.models import Writer
from blog.serializers import WriterDetailSerializer


class WriterDashboardViewSet(generics.ListAPIView):
    queryset = Writer.objects.annotate(
        total_articles=Count('written_articles'),
        total_recent_articles=Count(
            'written_articles',
            filter=Q(written_articles__created_at__gt=datetime.date.today() - datetime.timedelta(days=30))
        )
    ).all()
    serializer_class = WriterDetailSerializer
