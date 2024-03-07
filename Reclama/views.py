from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from Admin.models import *

# Create your views here.
class AddReclamaView(APIView):
    def post(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin:
            serializer = Reclamasrl(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Faqat adminlargina reclama qo'shishi mumkin")

class GetReclamaView(APIView):
    def get(self, request):
        serializer = Reclamasrl(Reclama, many = True)
        return Response(serializer.data)

class AddCategoryRecView(APIView):
    def post(self, request, id):
        admin = Admin.objects.filter(id=id).first()
        if admin:
            serializer = CategoryRecsrl(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Faqat adminlargina reclama qo'shishi mumkin")


class GetCategoryRecView(APIView):
    def get(self, request):
        serializer = CategoryRecsrl(Reclama, many = True)
        return Response(serializer.data)


class AddRecCardView(APIView):
    def post(self, request, id):
        admin = Admin.objects.filter(id=id).first()
        category = request.data.get('category')

        if admin:
            serializer = RecCardsrl(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Faqat adminlargina reclama qo'shishi mumkin")


class GetRecCardView(APIView):
    def get(self, request):
        serializer = RecCardsrl(Reclama, many=True)
        return Response(serializer.data)

