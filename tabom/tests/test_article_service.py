import django
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from tabom.models.article import Article
from tabom.models.like import Like
from tabom.models.user import User
from tabom.services.article_service import get_an_article, get_article_list
from tabom.services.like_service import do_like


class TestArticleService(TestCase):
    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title=title)

        # When
        result_article = get_an_article(article.id)

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(invalid_article_id)

    def test_get_article_list_should_prefetch_like(self) -> None:
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        like = do_like(user.id, articles[-1].id)

        with CaptureQueriesContext(connection) as ctx:
            with self.assertNumQueries(2):
                result_articles = get_article_list(0, 10)
                result_count = [a.like_set.count() for a in result_articles]

                self.assertEqual(len(result_articles), 10)
                self.assertEqual(1, result_count[0])
                self.assertEqual(
                    [a.id for a in reversed(articles[10:21])],
                    [a.id for a in result_articles],
                )

    def test_temp(self) -> None:
        user = User.objects.create(name="tester")
        article = Article.objects.create(title="test_title")
        like = Like.objects.create(user_id=user.id, article_id=article.id)
        Article.objects.create(title="test_title2")
        with CaptureQueriesContext(connection) as ctx:
            with self.assertNumQueries(1):
                result_like = Like.objects.select_related("user").get(id=like.id)
                self.assertEqual(like.id, result_like.id)

            with self.assertNumQueries(2):
                result_like = Like.objects.prefetch_related("user").get(id=like.id)
                self.assertEqual(like.id, result_like.id)
