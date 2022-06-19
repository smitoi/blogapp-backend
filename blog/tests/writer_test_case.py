import random
from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from blog.models import Article
from blog.tests.factories import ArticleFactory, WriterProfileFactory


class WriterTestCase(TestCase):
    def setUp(self):
        self.writer_profile = WriterProfileFactory()
        for _ in range(random.randint(5, 10)):
            ArticleFactory(written_by=self.writer_profile, status=Article.ArticleStatus.DRAFT)
        self.client = APIClient()
        self.client.force_authenticate(user=self.writer_profile.user)

    def test_writer_can_create_article(self):
        articlesCount = Article.objects.count()
        response = self.client.post('/api/article/', {
            'title': 'Title test',
            'content': 'You can use the tearDown method. It will be called after your test is run. '
                       'You can delete all Blahs there.',
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(articlesCount + 1, Article.objects.count())

    def test_writer_can_update_draft_article(self):
        article = ArticleFactory(written_by=self.writer_profile, status=Article.ArticleStatus.DRAFT)
        response = self.client.put(f'/api/article/{article.id}/', {
            'title': 'Title test',
            'content': 'You can use the tearDown method. It will be called after your test is run. '
                       'You can delete all Blahs there.',
        })
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_writer_can_update_rejected_article(self):
        article = ArticleFactory(written_by=self.writer_profile, status=Article.ArticleStatus.REJECTED)
        response = self.client.put(f'/api/article/{article.id}/', {
            'title': 'Title test',
            'content': 'You can use the tearDown method. It will be called after your test is run. '
                       'You can delete all Blahs there.',
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.ArticleStatus.DRAFT)

    def test_writer_cannot_update_approved_article(self):
        article = ArticleFactory(written_by=self.writer_profile, status=Article.ArticleStatus.APPROVED)
        response = self.client.put(f'/api/article/{article.id}/', {
            'title': 'Title test',
            'content': 'You can use the tearDown method. It will be called after your test is run. '
                       'You can delete all Blahs there.',
        })
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
