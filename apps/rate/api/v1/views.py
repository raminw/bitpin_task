import logging
from datetime import datetime

from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE, HTTP_400_BAD_REQUEST
from django.conf import settings

from apps.rate.services import RateService
from apps.rate.dtos import RateRedisObjectDTO
from apps.rate.models import Rate
from apps.rate.api.v1.serializers import RateSerializer


class RateView(generics.CreateAPIView):
    logger = logging.getLogger(__name__)

    queryset = Rate.objects.active()
    permission_classes = (IsAuthenticated,)
    serializer_class = RateSerializer

    @method_decorator(ratelimit(key='user_or_ip', rate=settings.CREATE_RATE_REQUEST_RATE_LIMIT))
    def create(self, request, *args, **kwargs):
        try:
            rate_serializer = RateSerializer(data=request.data)
            if rate_serializer.is_valid():
                valid_data = rate_serializer.validated_data
                rate_dto = RateRedisObjectDTO(
                    rater_id=request.user.id,
                    post_id=valid_data['post'].id,
                    score=valid_data['score'],
                    created_at=datetime.now()
                )
                RateService().add_rate_to_redis(rate_dto)
                return Response(status=HTTP_200_OK)
            else:
                return Response(data=rate_serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"function:[create] request:[{request}] error:[{e}]")
        return Response(status=HTTP_503_SERVICE_UNAVAILABLE)
