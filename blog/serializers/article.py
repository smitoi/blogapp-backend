from rest_framework import serializers
from blog.models import Article
from .writer import WriterSerializer


class ArticleWriterSerializer(serializers.ModelSerializer):
    written_by = WriterSerializer(read_only=True)
    edited_by = WriterSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'status', 'written_by', 'edited_by', 'created_at', ]
        read_only_fields = ['status', 'created_at', ]


class ArticleApprovalSerializer(serializers.ModelSerializer):
    written_by = WriterSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'status', 'written_by', 'created_at', ]
        read_only_fields = ['title', 'content', 'created_at', ]
