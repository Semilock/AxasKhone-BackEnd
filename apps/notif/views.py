from django.shortcuts import render

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView, status


@permission_classes((AllowAny,))
class SaveToDataBase(APIView):
    def post(self, request):
        print(request.META.get("REMOTE_ADDR"))
        if request.META.get("REMOTE_ADDR")=="127.0.0.1":
            print(request.data.get("data"))
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)