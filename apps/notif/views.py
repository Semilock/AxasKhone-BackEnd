from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import json


@permission_classes((AllowAny,))
class SaveToDataBase(APIView):
    def post(self, request):
        print(request.data.get("data"))
        return Response()