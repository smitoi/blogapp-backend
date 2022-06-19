import datetime

import factory
from django.conf import settings

from blog.models import Article, Writer


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('first_name')
    email = factory.Faker('ascii_email')
    password = factory.Faker('password')
    is_superuser = True

    class Meta:
        model = settings.AUTH_USER_MODEL


class WriterProfileFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('first_name')
    is_editor = False
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Writer


class ArticleFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=3)
    content = factory.Faker('sentence', nb_words=16)
    status = factory.Iterator(
        [Article.ArticleStatus.DRAFT, Article.ArticleStatus.APPROVED, Article.ArticleStatus.REJECTED])
    written_by = factory.Iterator([writer for writer in Writer.objects.all()])
    created_at = datetime.datetime.now()

    class Meta:
        model = Article

    @classmethod
    # See https://github.com/FactoryBoy/factory_boy/issues/102
    def _create(cls, target_class, *args, **kwargs):
        created_at = kwargs.pop('created_at', None)
        article = super(ArticleFactory, cls)._create(target_class, *args, **kwargs)
        if created_at is not None:
            article.created_at = created_at
            article.save()
        return article
