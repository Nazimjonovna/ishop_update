from rest_framework import serializers
from .models import *

class ParnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class EditPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['name', ]