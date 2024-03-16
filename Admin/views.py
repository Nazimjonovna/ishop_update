from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import random
import string
from .models import *
from .serializer import *
from Product.models import *
from Product.serializer import *

# Create your views here.
def generate_random_string(length):
    characters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(length))


def password_generate(length):
    l = [111111, 222222, 333333, 444444, 555555, 666666, 7777777, 888888, 999999]
    while True:
        a = random.randint(111111, 999999)
        if a not in l:
            return str(a)

class AddAdminView(APIView):
    def get(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin.is_boss:
            username = generate_random_string(6)
            password = password_generate(6)
            new_admin = Admin.objects.create(username = username, password = password)
            serializer = AdminSRL(new_admin)
            return Response(serializer.data)
        else:
            return Response("Yangi admin faqat superadmin tomonidan qo'shiladi!")


class LoginAdminview(APIView):
    @swagger_auto_schema(request_body = AdminSRL)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        admin = Admin.objects.filter(username = username, password = password).first()
        if admin:
            serializer = AdminSRL(admin)
            return Response({"Message":"Login successfully", 'data':serializer.data})
        else:
            return Response({"Message":"Uzr bazadan bunday admin topilmadi"})

class AddProtsent(APIView):
    @swagger_auto_schema(request_body = Protsentsrl)
    def post(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin:
            serializer = Protsentsrl(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Yangi protsent muvaffaqiyatli qo'shildi", 'data':serializer.data})
            else:
                return Response({"Message":"Xatolik mavjud", 'xato':serializer.errors})
        else:
            return Response({"Message":"Uzr bazada bunday admin topilmadi"})

class EditTasdiqView(APIView):
    @swagger_auto_schema(request_body = Protsentsrl)
    def patch(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin:
            info = request.data.get('product')
            product = Product.objects.filter(id = info.id).first()
            if product:
                product.tasdiq = True
                product.save()
                return Response({"Message":"Mahsulot satishga tasdiqlandi", 'data':list(product)})
            else:
                return Response({'Message':'Bunday Product topilmadi'})
        else:
            return Response({'Message':'Uzr bazada bunday admin topilmadi'})


class GetSonProduct(APIView):
    def get(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        t_son = 0
        tm_son = 0
        jami = 0
        tasdiqlangan = []
        tasdiqlanmagan = []
        if admin.is_boss:
            products = Product.objects.all()
            for product in products:
                if product.tasdiq:
                    t_son += 1
                    tasdiqlangan.append(product)
                else:
                    tm_son += 1
                    tasdiqlanmagan.append(product)
            jami = t_son + tm_son
            return Response({
                "Message":"Tasdiqlangan va tasdiqlanmagan tovarlar ro'yhati",
                "Jami mahsulotlar soni":str(jami),
                'Tasdiqlanganlar soni':str(t_son),
                'Tasdiqlanganlar':list(tasdiqlangan),
                'Tasdiqlanmaganlar soni': str(tm_son),
                'Tasdiqlanmaganlar':list(tasdiqlanmagan)
            })
        else:
            return Response({"Message":"uzr ushbu ma'lumotlar faqat boshliq uchun beriladi"})
        
class GetAdminProductsView(APIView):
    def get(self, request, id):
        quantity = {}
        admin = Admin.objects.filter(id = id).first()
        if admin.is_boss:
            admins = Admin.objects.all()
            for admin in admins:
                if admins.is_boss == False:
                    orders = Order.objects.filter(admin = admin)
                    quantity[f'{admin.name}'] = list(orders)
                else:
                    continue
            return Response({"Message":"Adminlar qo'shgan mahsulotlar haqida hisobot", 'data':quantity})
        else:
            return Response({"Message":"uzr ushbu ma'lumotlar faqat boshliq uchun beriladi"})



# orderla qop ketdi

class EditOrderStatusView(APIView):
    @swagger_auto_schema(request_body = OrderSerializer)
    def post(self, request, id):
        order = Order.objects.filter(id = id).first()
        if order:
            order.state = request.data.get('state')
            order.save()
            serializer = OrderSerializer(order)
            return Response({"Message":"Buyutma statusi o'zgartirildi", 'data':serializer.data})
        else:
            return Response({"Message":"Bunday buyurtma topilmadi"})
        
class GetOrderStatusView(APIView):
    def get(self, request, id):
        order_state = []
        admin = Admin.objects.filter(id = id).first()
        if admin:
            orders = Order.objects.all()
            for order in orders:
                if order.state == 'buyurtma_berish':
                    order_state.append(order)
                else:
                    continue
            serializer = OrderSerializer(order_state, many = True)
            return Response({"Message":"Aktiv buyurtmalar", 'data':serializer.data})
        else:
            return Response({"Message":"uzr ushbu ma'lumotlar faqat admin uchun beriladi"})



