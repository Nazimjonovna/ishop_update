from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from Admin.models import *
from User.models import User
from Admin.models import *

# Create your views here.
class CreateCategoryView(APIView):
    """ Admin yangi category qoshadi """

    def update_choise(self):
        """ qo'shilgan category ni choise qilib chaqarish """
        category_names = Category.objects.values_list('name', flat=True)
        Category._meta.get_field('name').choices = [(name, name) for name in category_names]

    def post(self, request, id):
        """ Faqat admin qo'shishini ta'minlash uchun id bilan tekshiriladi """
        admin = Admin.objects.filter(id = id).first()
        if admin:
            serializer = CreateCategorySerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                self.update_choise()
                return Response({"Message":"Category qo'shildi", 'data':serializer.data})
            else:
                return Response({"Message":"Xato mavjud", 'error':serializer.errors})
        else:
            return Response({"Message":"Uzr siz admin emasligingiz sababli category qo'sha olmaysz)"})


class CreateSubCategoryView(APIView):
    """ Admin yangi subcategory qoshishi """

    def update_choise(self):
        """ qo'shilgan subcategory ni choise qilib chaqarish """
        category_names = SubCategory.objects.values_list('name', flat=True)
        SubCategory._meta.get_field('name').choices = [(name, name) for name in category_names]

    def post(self, request, id):
        """ Faqat admin qo'shishini ta'minlash uchun id bilan tekshiriladi """
        admin = Admin.objects.filter(id = id).first()
        if admin:
            serializer = CreateSubCategorySerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                self.update_choise()
                return Response({"Message":"SubCategory qo'shildi", 'data':serializer.data})
            else:
                return Response({"Message":"Xato mavjud", 'xato':serializer.errors})
        else:
            return Response({"Message":"Uzr siz admin emasligingiz sababli category qo'sha olmaysz)"})


class AddProdcutView(APIView):
    """ Faqat admin qo'shishini ta'minlash uchun id bilan tekshiriladi
        Yangi product qo'shish. Bunda hamma ma'lumotlarni bitta serializer
        bilan tekshirib olinadi."""

    def post(self, request, id):
        admin = Admin.objects.filter(id = id).first()
        if admin:
            serializer = ProductSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Mahsulot qo'shildi", "data":serializer.data})
            else:
                return Response({"Message":"Mahsulotni qo'shishda xatolik mavjud", "xato":serializer.errors})
        else:
            return Response({"Message":"Uzr siz admin emasligingiz sababli category qo'sha olmaysz)"})

class EditProduct(APIView):
    """ Product haqidagi ma'luumotlar ustida ishlash view si.
        Bunda 1ta product ma'lumotlarini olish, o'zgartirish yokida
        o'chirish imkoniyati mavjud."""

    def get(self, request, id):
        product = Product.objects.filter(id = id).first()
        if product:
            pro = ProductSerializer(product)
            i = ProductInfo.objects.filter(product = product)
            info = ProductInfoSerializer(i, many=True)
            r = Image.objects.filter(product = product)
            image = ImageSerializer(r, many=True)
            return Response({"Message":"Siz tanlagan mahsulot haqida ma'lumotlar",
                             "product": pro.data,
                             'info': info.data,
                             'image': image.data})
        else:
            return Response({"Message":"Uzr siz tanlagan mahsulot bazada topilmadi)"})

    def patch(self, request, id):
        product = Product.objects.filter(id = id).first()
        if product:
            serializer = ProductSerializer(instance=product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Mahsulot muvaffaqiyatli o'zgartirildi", 'data':serializer.data})
            else:
                return Response({"Message": "Mahsulotni o'zgartirishda xatolik mavjud", "xato":serializer.errors})
        else:
            return Response({"Message":"Uzr siz tanlagan mahsulot bazada topilmadi)"})

    def delete(self, request, id):
        """ Bunda Product va ProductInfo hamda Image modellari o'zaro
            on_delete funksiyati bilan bog'langanligi sababli alohida
            o'chirilishi shart emas product o'chsa info va image ham o'chadi"""
        product = Product.objects.filter(id = id).first()
        if product:
            product.delete()
            return Response({"Message":"Kiritgan mahsulotingiz muvaffaqiyatli o'chirildi)"})
        else:
            return Response({"Message": "Uzr siz tanlagan mahsulot bazada topilmadi)"})


class GetProductView(APIView):
    def get(self,request):
        products = Product.objects.filter(tasdiq = True)
        result = {"products": []}
        for product in products:
            i = ProductInfo.objects.filter(product=product)
            info = ProductInfoSerializer(i, many=True)
            r = Image.objects.filter(product=product)
            image = ImageSerializer(r, many=True)
            pro = ProductSerializer(product).data
            result['products'].append(pro)
        return Response({"Message":"Mahsulotlar ro'yhati", "products":result})


class PostOrderView(APIView):
    def post(self, request, id):
        user = User.objects.filter(id = id).first()
        if user:
            serializer = OrderSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Buyurtma qabul qilindi", "data":serializer.data})
            else:
                return Response({"Message":f"Sizdagi xatolik---{serializer.errors}"})
        else:
            return Response({"Message":"Siz hali ro'yhatdan o'tmagansiz"})

class GetOrderView(APIView):
    def get(self, request, id):
        summa = 0
        user = User.objects.filter(id = id).first()
        if user:
            orders = Order.objects.filter(user = user)
            if order:
                for order in orders:
                    summa += order.cost_order
                serializer = OrderSerializer(orders, many = True)
                return Response({"Message":"Sizning barcha buyurtmalaringiz", 'data':serializer.data, "allsumm":str(summa)})
            else:
                return Response({"Message":"Sizda hozircha aktiv buyurtmalar topilmadi"})
        else:
            return Response({"Messsage":"Siz hali ro'yhatdan o'tmagansiz"})
        
    
class GetOneOrderView(APIView):
    def get(self, request, id):
        order = Order.objects.filter(id = id).first()
        if order:
            if order.payment == 'credit':
                cost = order.product.cost
                oy = order.oy
                name = order.name_credit
                protsent = Protsent.objects.filter(name = name).first()
                order_summ = float(cost)*(1+float(protsent/100))*float(order.quantity)/float(oy)
                serializer = OrderSerializer(order)
                return Response({"Message":f"Sizning buyurtmangiz---{serializer.data}", "allsumm":str(order_summ)})
            elif order.payment == 'naqt' and order.payment == 'card':
                cost = order.product.cost
                order_summ = float(cost) * float(order.quantity)
                serializer = Order(order)
                return Response({"message":f"Sizning buyurtmangiz---{serializer.data}", "allsumm":str(order_summ)})
            else:
                return Response({"Message":"To'lov turi kiritilmagan"})
            
        else:
            return Response({"Message":"Sizda hozircha aktiv buyurtma yoq"})
        

class OrderEditView(APIView):
    def patch(self, request, id):
        order = Order.objects.filter(id = id).first()
        if order:
            serializer = OrderSerializer(instanse = order, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Sizning buyurtmangiz muvaffiqiyatli o'zgartirildi", 'data':serializer.data})
            else:
                return Response({"Message":f"Sizning erroringiz---{serializer.errors}"})
        else:
            return Response({"Message":"Bunday order yoq"})
        
    def delete(self, request, id):
        order = Order.objects.filter(id = id).first()
        if order:
            order.delete()
            return Response({"Message":"Buyurtma bekor qilindi"})
        else:
            return Response({"Message":"Bunday buyurtma topilmadi"})
        
class BasketView(APIView):
    def get(self, request, id):
        basket = []
        pro = []
        pro_info = []
        images = []
        user = User.objects.filter(id = id).first()
        if user:
            orders = Order.objects.filter(user = user)
            for order in orders:
                if order.state == 'buyurtma_berish' and order.pro_x == "is_buy" or order.pro_x == 'is_like':
                    product = Product.objects.get(id = order.product)
                    img = Image.objects.filter(product = order.product)
                    info = ProductInfo.objects.filter(product = order.product)
                    basket.append(order)
                    pro.append(product)
                    pro_info.append(info)
                    images.append(img)
                else:
                    continue
            serializer = OrderSerializer(basket, many = True)
            seri_product = ProductSerializer(pro, many = True)
            seri_info = ProductInfoSerializer(pro_info, many = True)
            seri_img = ImageSerializer(images, many =True)
            return Response({"Message":"Sizning savatchangiz", 
                             'order':serializer.data,
                             'product':seri_product.data,
                             'info':seri_info.data,
                             'images':seri_img.data})
        else:
            return Response({'Message':"Siz ro'yhatdan o'tmagansiz"})
        
        
        
class GetLikedOrdersView(APIView):
    def get(self, request, id):
        basket = []
        pro = []
        pro_info = []
        images = []
        user = User.objects.filter(id = id).first()
        if user:
            orders = Order.objects.filter(user = user)
            for order in orders:
                if order.pro_x == 'is_like':
                    product = Product.objects.get(id = order.product)
                    img = Image.objects.filter(product = order.product)
                    info = ProductInfo.objects.filter(product = order.product)
                    basket.append(order)
                    pro.append(product)
                    pro_info.append(info)
                    images.append(img)
                else:
                    continue
            serializer = OrderSerializer(basket, many = True)
            seri_product = ProductSerializer(pro, many = True)
            seri_info = ProductInfoSerializer(pro_info, many = True)
            seri_img = ImageSerializer(images, many =True)
            return Response({"Message":"Sizning savatchangiz", 
                             'order':serializer.data,
                             'product':seri_product.data,
                             'info':seri_info.data,
                             'images':seri_img.data})
        else:
            return Response({'Message':"Siz ro'yhatdan o'tmagansiz"})


        

            



        

            


