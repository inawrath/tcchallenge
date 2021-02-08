from rest_framework import serializers

from core.models import AssetData


class AssetDataSerializer(serializers.ModelSerializer):

    def to_representation(self, instance: AssetData):
        representation: dict = {
            instance.data_datetime.strftime('%Y-%m-%d %H:%M'): {
                'price': instance.price,
                'low_24h': instance.low_24h,
                'high_24h': instance.high_24h,
                'returns_24h': instance.returns_24h,
                'returns_ytd': instance.returns_ytd,
                'volatility': instance.volatility,
            }
        }

        return representation

    class Meta:
        model = AssetData
        exclude = (
            'id',
            'asset',
            'creation_date',
        )
