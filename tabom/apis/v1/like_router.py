from typing import Tuple

from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from tabom.apis.v1.schemas.like_request import LikeRequest
from tabom.apis.v1.schemas.like_response import LikeResponse
from tabom.models import Like
from tabom.models.article import Article
from tabom.models.user import User
from tabom.services.like_service import do_like, undo_like

router = Router(tags=["likes"])


@router.post("/", response={201: LikeResponse})
def post_like(request: HttpRequest, like_request: LikeRequest) -> Tuple[int, Like]:
    try:
        like = do_like(like_request.user_id, like_request.article_id)
    except User.DoesNotExist:
        raise HttpError(404, f"User #{like_request.user_id} Not Found")
    except Article.DoesNotExist:
        raise HttpError(404, f"Article #{like_request.article_id} Not Found")
    except IntegrityError:
        raise HttpError(400, "duplicate like")
    return 201, like


@router.delete("/", response={204: None})
def delete_like(request: HttpRequest, user_id: int, article_id: int) -> Tuple[int, None]:
    undo_like(user_id, article_id)
    return 204, None
