from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favourite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию

        validated_data = super().validate(data)
        user = self.context['request'].user
        ads = Advertisement.objects.filter(creator=user).filter(status='OPEN').all()

        if len(ads) >= 10 and validated_data['status'] == 'OPEN':
            raise ValidationError('Too much opened ads. Maximum quantity is 10!')

        return data

    def destroy(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().perform_destroy(validated_data)


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ('id', 'user', 'ad')

