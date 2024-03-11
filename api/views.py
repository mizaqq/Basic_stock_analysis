from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import CompanySerializer
from base.models import Company
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getData(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies,many=True)
    return Response(serializer.data)
