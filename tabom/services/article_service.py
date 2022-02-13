from tabom.models.article import Article


def get_an_article(article_id: int) -> Article:
    return Article.objects.filter(id=article_id).get()
