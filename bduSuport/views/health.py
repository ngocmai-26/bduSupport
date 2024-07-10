from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.request import Request

class HealthView(ViewSet):
    authentication_classes = ()

    @action(["GET"], detail=False, url_path="check")
    def health(self, request: Request):
        return Response(status=HTTP_200_OK)