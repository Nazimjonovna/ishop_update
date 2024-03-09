from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializer import *
from Admin.models import Admin

# Create your views here.
class PostPartnerView(APIView):
    def post(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin.is_boss:
            serializer = ParnerSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Hamkor qo'shildi", 'data':serializer.data})
            else:
                return Response({"Message":f"Sizning xatoyingiz---{serializer.errors}"})
        else:
            return Response({"Message":"Hamkorlarni qo'shish faqat superadmin uchun"})
        
class GetPartnerView(APIView):
    def get(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin:
            serializer = ParnerSerializer(Partner, many =True)
            return Response({"Message":"Hamkorlar ro'yhati", 'data':serializer.data})
        else:
            return Response({"Message":"Hamkorlarni qo'shish faqat admin uchun"})
        
class EditPartnerView(APIView):
    @swagger_auto_schema(request_body = EditPartnerSerializer)
    def post(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin.is_boss:
            partner = Partner.objects.filter(name = request.data.get('name')).first()
            serializer = ParnerSerializer(partner, many = True)
            return Response({"Message":"Izlagan hamkoringiz", 'data':serializer.data})
        else:
            return Response({"Message":"Bu amaliyotni faqat superadmin amalga oshira oladi"})
        
    @swagger_auto_schema(request_body = EditPartnerSerializer)
    def patch(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin.is_boss:
            partner = Partner.objects.filter(name = request.data.get('name')).first()
            serializer = ParnerSerializer(instance = partner, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Hamkor ma'lumotlari o'zgartirildi", 'data':serializer.data})
            else:
                return Response({"Message"f"Sizning xatoyingiz---{serializer.errors}"})
        else:
            return Response({"Message":"Bu amaliyotni faqat superadmin amalga oshira oladi"})
        
    @swagger_auto_schema(request_body = EditPartnerSerializer)
    def delete(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin.is_boss:
            partner = Partner.objects.filter(name = request.data.get('name')).first()
            partner.delete()
            return Response({"Message":"Hamkor o'chirildi"})
        else:
            return Response({"Message":"Bu amaliyotni faqat superadmin amalga oshira oladi"})
        

        
    

