from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
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
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filter_class = [AdvertisementFilter]
    filterset_fields = ['status', 'created_at', 'creator__id']


    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", ]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        return []

    def list(self, request, *args, **kwargs):
        queryset = Advertisement.objects.all()

        if request.user.is_anonymous:
            self.queryset = queryset.filter(status='OPEN')
        elif request.user.is_superuser:
            self.queryset = queryset
        else:
            self.queryset = queryset.filter(status='OPEN') | queryset.filter(creator=request.user)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def fav(self, request, pk=None):
        user = request.user
        ad = Advertisement.objects.get(id=pk)

        if user != ad.creator:
            new_fav = Favourite(user=user, ad=ad)
            new_fav.save()
            return Response({"status": f"Ad with number {pk} set as favorite"})
        else:
            return Response('You cannot add to favs ads created by you')

    @action(detail=False, methods=['GET'])
    def favs(self, request):
        user = request.user
        favs = Favourite.objects.filter(user=user).all()
        serializer = FavouriteSerializer(favs, many=True)
        return Response(serializer.data)
