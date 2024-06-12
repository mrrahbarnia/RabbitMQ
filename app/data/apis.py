from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request

from drf_spectacular.utils import extend_schema

from . import services


class InsertDataApi(APIView):

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=80)
        content = serializers.CharField(max_length=1000)

    @extend_schema(request=InputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        services.insert_data(
            title=input_serializer.validated_data.get('title'),
            content=input_serializer.validated_data.get('content')
        )
        return Response(
            {'message': 'HSET successfully'},
            status=status.HTTP_201_CREATED
        )


class ListDataApi(APIView):

    def get(self, request: Request, *args, **kwargs) -> Response:
        data = services.list_titles()
        return Response(data, status=status.HTTP_200_OK)
