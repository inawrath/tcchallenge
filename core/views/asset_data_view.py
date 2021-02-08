import http

from rest_framework import generics
from rest_framework.response import Response

from core.models import (
    Asset,
    AssetData,
)
from core.serializers import AssetDataSerializer
from core.utils import get_first_element


class AssetDataList(generics.ListAPIView):
    serializer_class = AssetDataSerializer
    pagination_class = None
    MAX_RESULTS = 30

    def get_queryset(self):
        return AssetData.objects.filter(
            asset__name=self.kwargs['name'],
        ).order_by('data_datetime')[:self.MAX_RESULTS]

    def list(self, request, **kwargs):
        asset: Asset = Asset.objects.filter(name=kwargs['name'])

        if len(asset) == 0:
            return Response({}, status=http.HTTPStatus.NOT_FOUND)

        queryset = self.get_queryset()
        serializer = AssetDataSerializer(queryset, many=True)

        response: dict = {
            'asset': asset[0].name,
            'values': {
                get_first_element(x.keys()): get_first_element(x.values())
                for x in serializer.data
            },
        }

        return Response(response)
