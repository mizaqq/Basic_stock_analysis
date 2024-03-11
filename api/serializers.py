from base.models import Company
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'