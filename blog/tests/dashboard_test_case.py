import datetime
import random
from django.test import TestCase

from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from blog.models import Writer, Article
from blog.tests.factories import ArticleFactory, WriterProfileFactory


class DashboardTestCase(TestCase):
    def test_dashboard_displays_correctly(self):
        writer_profile = WriterProfileFactory()
        published_articles = random.randint(0, 10)
        published_recent_articles = random.randint(0, 10)

        for _ in range(min(0, published_articles - published_recent_articles)):
            ArticleFactory(written_by=writer_profile)

        for _ in range(published_articles):
            ArticleFactory(written_by=writer_profile,
                           created_at=datetime.date.today() - datetime.timedelta(days=random.randint(30, 60)))

        client = APIClient()
        client.force_authenticate(user=writer_profile.user)
        response = client.get(f'/api/writer/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), len(Writer.objects.all()))
        for writer in data:
            self.assertEqual(writer['total_articles'], Article.objects.filter(written_by_id=writer['user_id']).count())
            self.assertEqual(writer['total_recent_articles'],
                             Article.objects.filter(written_by_id=writer['user_id'],
                                                    created_at__gt=datetime.date.today() - datetime.timedelta(
                                                        days=30)).count())
