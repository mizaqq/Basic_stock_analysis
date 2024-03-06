from . import models
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'