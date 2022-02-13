from django.core.paginator import Paginator
from django.db.models import QuerySet

from tabom.models.article import Article


def get_an_article(article_id: int) -> Article:
    return Article.objects.filter(id=article_id).get()


def get_article_list(offset: int, limit: int) -> QuerySet[Article]:
    return Article.objects.order_by("-id").prefetch_related("like_set")[offset : offset + limit]
