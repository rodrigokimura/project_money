from datetime import datetime

from http import HTTPStatus
from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.db import transaction
from django.db.models import Aggregate, Count, Q, Sum
from django.views.decorators.cache import cache_page
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import TransactionCategory
from .utils import process, sync


def get_filter(reference: datetime, months: int):
    d = reference + relativedelta(months=-months)

    return Q(
        transaction__timestamp__month=d.month,
        transaction__timestamp__year=d.year,
    )


def get_annotation():
    now = datetime.now()
    f: dict[str, Aggregate] = {}
    for i in range(12):
        f[f"count_{i}"] = Count("transaction__id", filter=get_filter(now, i))
        f[f"sum_{i}"] = Sum("transaction__amount", filter=get_filter(now, i))

    return f


@cache_page(60 * 60)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def categories(_: Request):
    categories = TransactionCategory.objects.annotate(**get_annotation()).values(
        "name",
        *[f"count_{i}" for i in range(12)],
        *[f"sum_{i}" for i in range(12)],
    )

    result = {
        record.get("name"): {
            **record,
            **{
                f"sum_{i}": round(float(record.pop(f"sum_{i}") or 0), 2)
                for i in range(12)
            },
        }
        for record in categories
    }

    return Response(result)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic()
def force_sync(_: Request):
    sync()
    process()
    cache.clear()
    return Response({"message": "Synced successfully!"}, status=HTTPStatus.CREATED)
