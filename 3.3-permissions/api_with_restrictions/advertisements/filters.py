from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    status = filters.CharFilter()
    created_at = filters.DateFromToRangeFilter()
    creator = filters.NumberFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'created_at', 'creator__id']
