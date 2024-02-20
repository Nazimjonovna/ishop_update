from rest_framework import serializers
from .models import *

class Reclamasrl(serializers.ModelSerializer):
    class Meta:
        model = Reclama
        fields = '__all__'


class CategoryRecsrl(serializers.ModelSerializer):
    class Meta:
        model = Categoryreclama
        fields = '__all__'


# class 8600061021054431
class RecCardsrl(serializers.ModelSerializer):
    class Meta:
        model = RecCard
        fields = '__all__'