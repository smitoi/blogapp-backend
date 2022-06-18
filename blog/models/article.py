from django.db import models
from .writer import Writer


class Article(models.Model):
    class ArticleStatus(models.TextChoices):
        DRAFT = ('draft', 'Draft')
        APPROVED = ('approved', 'Approved')
        REJECTED = ('rejected', 'Rejected')

    title = models.CharField(max_length=256)
    content = models.TextField()
    status = models.CharField(max_length=16, choices=ArticleStatus.choices, default=ArticleStatus.DRAFT)
    written_by = models.ForeignKey(Writer, on_delete=models.SET_NULL, related_name='written_articles', null=True)
    edited_by = models.ForeignKey(Writer, on_delete=models.SET_NULL, related_name='edited_articles', null=True,
                                  default=None)
    created_at = models.DateTimeField(auto_now_add=True)
