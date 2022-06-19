import random
from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from blog.models import Article
from blog.tests.factories import ArticleFactory, WriterProfileFactory


class EditorTestCase(TestCase):
    def setUp(self):
        self.writer_profile = WriterProfileFactory()
        for _ in range(random.randint(5, 10)):
            ArticleFactory(written_by=self.writer_profile, status=Article.ArticleStatus.DRAFT)
        self.editor_profile = WriterProfileFactory(is_editor=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.editor_profile.user)
        for _ in range(random.randint(5, 10)):
            ArticleFactory(written_by=self.writer_profile, edited_by=self.editor_profile,
                           status=Article.ArticleStatus.APPROVED if random.random() > 0.5
                           else Article.ArticleStatus.REJECTED)

    def test_editor_can_see_reviewed_articles(self):
        response = self.client.get(f'/api/articles-edited/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), Article.objects.filter(edited_by=self.editor_profile).count())

    def test_editor_can_view_pending_articles(self):
        response = self.client.get(f'/api/article-approval/')
        self.assertEqual(len(response.json()), Article.objects.filter(status=Article.ArticleStatus.DRAFT).count())

    def __change_status_test(self, status):
        article = ArticleFactory(written_by=self.writer_profile, status=Article.ArticleStatus.DRAFT)
        response = self.client.put(f'/api/article-approval/{article.id}/', {
            'status': status,
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        article.refresh_from_db()
        self.assertEqual(article.status, status)
        self.assertEqual(article.edited_by_id, self.editor_profile.user_id)

    def test_editor_can_approve_article(self):
        self.__change_status_test(Article.ArticleStatus.APPROVED)

    def test_editor_can_reject_article(self):
        self.__change_status_test(Article.ArticleStatus.REJECTED)

    def test_writer_cannot_update_status(self):
        self.client.force_authenticate(self.writer_profile.user)
        article = Article.objects.filter(edited_by__isnull=True).first()
        response = self.client.put(f'/api/article-approval/{article.id}/', {
            'status': Article.ArticleStatus.APPROVED,
        })
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
