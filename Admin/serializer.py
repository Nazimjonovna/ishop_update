from rest_framework import serializers
from .models import *
from Product.models import *

class AdminSRL(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class Protsentsrl(serializers.ModelSerializer):
    class Meta:
        model = Protsent
        fields = '__all__'


class EditTasdiqsrl(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"