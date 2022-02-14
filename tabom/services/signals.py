from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from tabom.models import Article, Like

# @receiver(post_save, sender=Like)
# def add_like_count(sender, instance, **kwargs):
#     Article.objects.filter(id=instance.article_id).update(like_count=F("like_count") + 1)


# @receiver(post_delete, sender=Like)
# def sub_like_count(sender, instance, **kwargs):
#     Article.objects.filter(id=instance.article_id).update(like_count=F("like_count") - 1)
