from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from tabom.models.article import Article
from tabom.models.like import Like
from tabom.models.user import User
from tabom.services.article_service import (
    create_an_article,
    delete_an_article,
    get_an_article,
    get_article_list,
)
from tabom.services.like_service import do_like


class TestArticleService(TestCase):
    def test_you_can_create_an_artice(self) -> None:
        # Given
        title = "test_title"

        # When
        article = create_an_article(title)

        # Then
        self.assertEqual(article.title, title)

    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = create_an_article(title)

        # When
        result_article = get_an_article(0, article.id)

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(0, invalid_article_id)

    def test_get_article_list_should_prefetch_like(self) -> None:
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        like = do_like(user.id, articles[-1].id)

        with CaptureQueriesContext(connection) as ctx:
            with self.assertNumQueries(3):
                result_articles = get_article_list(user.id, 0, 10)
                result_count = [a.like_count for a in result_articles]

                self.assertEqual(len(result_articles), 10)
                self.assertEqual(1, result_count[0])
                self.assertEqual(
                    [a.id for a in reversed(articles[10:21])],
                    [a.id for a in result_articles],
                )

    def test_temp(self) -> None:
        user = User.objects.create(name="tester")
        article = create_an_article("test_title")
        like = Like.objects.create(user_id=user.id, article_id=article.id)
        Article.objects.create(title="test_title2")
        with CaptureQueriesContext(connection) as ctx:
            with self.assertNumQueries(1):
                result_like = Like.objects.select_related("user").get(id=like.id)
                self.assertEqual(like.id, result_like.id)

            with self.assertNumQueries(2):
                result_like = Like.objects.prefetch_related("user").get(id=like.id)
                self.assertEqual(like.id, result_like.id)

    def test_get_article_list_should_contain_my_likes_when_like_exists(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article1 = create_an_article("article1")
        like = do_like(user.id, article1.id)
        Article.objects.create(title="article2")

        # When
        articles = get_article_list(user.id, 0, 10)

        # Then
        self.assertEqual(like.id, articles[1].my_likes[0].id)
        self.assertEqual(0, len(articles[0].my_likes))

    def test_get_article_list_should_not_contain_my_likes_when_user_id_is_zero(self) -> None:
        user = User.objects.create(name="test")
        article = create_an_article("test_title")
        Like.objects.create(user_id=user.id, article_id=article.id)
        Article.objects.create(title="test_title2")
        invalid_user_id = 0

        articles = get_article_list(invalid_user_id, 0, 10)

        self.assertEqual(0, len(articles[1].my_likes))
        self.assertEqual(0, len(articles[0].my_likes))

    def test_you_can_delete_an_article(self) -> None:
        # Given
        user = User.objects.create(name="user1")
        article = create_an_article("test_title")
        like = do_like(user.id, article.id)

        # When
        delete_an_article(article.id)

        # Then
        self.assertFalse(Article.objects.filter(id=article.id).exists())
        self.assertFalse(Like.objects.filter(id=like.id).exists())
