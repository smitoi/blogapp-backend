from rest_framework import serializers
from blog.models import Writer


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['name', 'is_editor', 'user_id']


class WriterDetailSerializer(serializers.ModelSerializer):
    total_articles = serializers.IntegerField(read_only=True)
    total_recent_articles = serializers.IntegerField(read_only=True)

    class Meta:
        model = Writer
        fields = ['name', 'is_editor', 'user_id', 'total_articles', 'total_recent_articles']
