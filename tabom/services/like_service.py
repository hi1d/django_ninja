from tabom.models.article import Article
from tabom.models.like import Like
from tabom.models.user import User
from django.db.models import F
# from django.db import transaction
# import tabom.services.signals




# @transaction.atomic
def do_like(user_id: int, article_id: int) -> Like:
    User.objects.filter(id=user_id).get()
    article = Article.objects.filter(id=article_id).get()
    Article.objects.filter(id=article_id).update(like_count=F("like_count") + 1)
    like = Like.objects.create(user_id=user_id, article_id=article_id)

    return like



def undo_like(user_id: int, article_id: int) -> None:
    deleted_cnt, _ = Like.objects.filter(user_id=user_id, article_id=article_id).delete()
    if deleted_cnt:
        Article.objects.filter(id=article_id).update(like_count=F("like_count")+1)
        
