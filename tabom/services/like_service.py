from tabom.models.like import Like
from tabom.models.user import User


def do_like(user_id: int, article_id: int) -> Like:
    return Like.objects.create(user_id=user_id, article_id=article_id)


def undo_like(user_id: int, article_id: int) -> None:
    like = Like.objects.filter(user_id=user_id, article_id=article_id).delete()
