from django.http import response
from django.test import TestCase

from tabom.models import Like, User
from tabom.models.article import Article
from tabom.services.article_service import create_an_article
from tabom.services.like_service import do_like


class TestLikeRouter(TestCase):
    def test_post_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article = create_an_article("test_title")

        # When
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user.id,
                "article_id": article.id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual(user.id, response.json()["user_id"])

    def test_delete_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = create_an_article("test_title")
        like = do_like(user.id, article.id)

        # When
        response = self.client.delete(f"/api/v1/likes/?user_id={user.id}&article_id={article.id}")

        # Then
        self.assertEqual(204, response.status_code)
        self.assertFalse(Like.objects.filter(id=like.id).exists())

    def test_post_lie_user_does_not_exist(self) -> None:
        invalid_user_id = 9988
        article = create_an_article("test_title")

        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": 9988,
                "article_id": article.id,
            },
            content_type="application/json",
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(f"User #{invalid_user_id} Not Found", response.json()["detail"])

    def test_post_like_article_does_not_exist(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        invalid_article_id = 9988

        # When
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user.id,
                "article_id": invalid_article_id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual(f"Article #{invalid_article_id} Not Found", response.json()["detail"])

    def test_post_like_duplicate_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = create_an_article("test_title")
        do_like(user.id, article.id)

        # When
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user.id,
                "article_id": article.id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(400, response.status_code)
        self.assertEqual(f"duplicate like", response.json()["detail"])

    # delete like

    def test_delete_non_existing_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = create_an_article("test_title")

        # When
        response = self.client.delete(f"/api/v1/likes/?user_id={user.id}&article_id={article.id}")

        # Then
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Article.objects.filter(id=article.id).get().like_count)
