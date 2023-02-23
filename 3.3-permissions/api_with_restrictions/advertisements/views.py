from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favourite
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer, FavouriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filter_class = [AdvertisementFilter]
    filterset_fields = ['status', 'created_at', 'creator__id']


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", ]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    def list(self, request, *args, **kwargs):
        queryset = Advertisement.objects.filter(status='OPEN')
        if request.user.is_authenticated:
            queryset = queryset.union(Advertisement.objects.filter(status='DRAFT', creator=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)