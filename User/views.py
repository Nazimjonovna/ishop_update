import requests
import pytz
import datetime as d
from random import randint
from rest_framework import generics
from django.conf import settings
from get_sms import Getsms
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from .models import *
from .serializer import *

# Create your views here.
utc = pytz.timezone(settings.TIME_ZONE)
min = 1

# Create your views here.
def send_sms(phone_number, step_reset=None, change_phone=None):
    try:
        verify_code = randint(111111, 999999)
        try:
            obj = Verification.objects.get(phone=phone_number)
        except Verification.DoesNotExist:
            obj = Verification(phone=phone_number, verify_code=verify_code)
            obj.step_reset = step_reset
            obj.step_change_phone = change_phone
            obj.save()
            context = {'phone_number': str(obj.phone), 'verify_code': obj.verify_code,
                       'lifetime': _(f"{min} minutes")}
            return context
        time_now = d.datetime.now(utc)
        diff = time_now - obj.created
        three_minute = d.timedelta(minutes=min)
        if diff <= three_minute:
            time_left = str(three_minute - diff)
            return {'message': _(f"Try again in {time_left[3:4]} minute {time_left[5:7]} seconds")}
        obj.delete()
        obj = Verification(phone=phone_number)
        obj.verify_code = verify_code
        obj.step_reset = step_reset
        obj.step_change_phone = change_phone
        obj.save()
        context = {'phone_number': str(obj.phone), 'verify_code': obj.verify_code, 'lifetime': _(f"{min} minutes")}
        return context
    except Exception as e:
        print(f"\n[ERROR] error in send_sms <<<{e}>>>\n")

# requests.post("http://sms-service.m1.uz/send_sms/", {"phone_number": 998901361752, "text": "Hello"})


class SendSms(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendSmsSerializer

    def post(self, request):
        serializer = SendSmsSerializer(data=request.data)
        if serializer.is_valid():
            login = "Name_of_work"
            password = "B180Ns49DnRbuPX9686R"
            nickname = "ShopUz"

            message = Getsms(login=login, password=password, nickname=nickname)
            phone_numbers = [serializer.data['phone_number']]

            results = message.send_message(phone_numbers=phone_numbers, text=serializer.data['text'])

            if 'error' in results:
                print(results)

            for result in results:
                print(result)
            return Response({"msg": f"Send SMS successfully to {serializer.data['phone_number']}"})
        else:
            return Response({"msg": serializer.errors})


class PhoneView(APIView):

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Phone'])
    def post(self, request):
        phone_number = request.data.get("phone")
        if phone_number is not None and phone_number.isdigit() and len(phone_number) > 8:
            user = User.objects.filter(phone__iexact=phone_number)
            if user.exists():
                return Response({
                    "status": False,
                    "detail": "Bu raqam avval registerdan otgan."
                })
            else:
                otp = send_sms(phone_number)
                if 'verify_code' in otp:
                    code = str(otp['verify_code'])
                    try:
                        validate = ValidatedOtp.objects.get(phone=phone_number)
                        if validate.validated:
                            validate.otp = code
                            validate.validated = False
                            validate.save()

                    except ValidatedOtp.DoesNotExist as e:
                        phon = ValidatedOtp.objects.filter(phone__iexact=phone_number)
                        if not phon.exists():
                            ValidatedOtp.objects.create(phone=phone_number, otp=code, validated=False)
                        else:
                            Response({"phone": "mavjud"})

                return Response({
                    "status": True,
                    "detail": "SMS xabarnoma jo'natildi",
                    "code": otp  # <--vaqtinchalik qo'shildi
                })
        else:
            if phone_number is not None and len(phone_number) < 8:
                return Response({"detail": "Telefon raqamingizni kod bilan kiriting!"})
            else:
                return Response({
                    "status": False,
                    "detail": "Telefon raqamni kiriting ."
                })

    def send_otp(phone, otp):
        if phone:
            otp = randint(111111, 999999)
            print(otp)
            return otp
        else:
            return False

class OtpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=OtpSRL, tags=['Register'])
    def post(self, request):
        phone_number = request.data.get('phone', True)
        code_send = request.data.get('otp', True)
        if not phone_number and code_send:
            return Response({
                'status': False,
                'detail': 'Otpni va phone ni kiriting'
            })

        try:
            verify = ValidatedOtp.objects.get(phone=phone_number, validated=False)
            if verify.otp == code_send:
                verify.count += 1
                verify.validated = True
                verify.save()

                return Response({
                    'status': True,
                    'detail': "Otp to'g'ri"
                })
            else:
                return Response({
                    'status': False,
                    'error': "Otpni to'g'ri kiriting"})

        except ValidatedOtp.DoesNotExist as e:
            return Response({
                'error': "Otp aktiv emas yoki mavjud emas, boshqa otp oling"
            })


class RegisterViewNaqt(APIView):
    permission_classes = [AllowAny]
    serializer_classes = Register

    @swagger_auto_schema(request_body=Register, tags=['Register'])
    def post(self, request):
        request.POST._mutable = True
        password = request.data['password'][:]
        request.data['password'] = make_password(password)
        serializer = True
        request.POST._mutable = True

        try:
            verify = ValidatedOtp.objects.filter(phone__iexact=request.data['phone'], validated=True)
            if verify.exists():
                if serializer:
                    user_obj = User(phone=request.data['phone'])
                    user_obj.password = request.data['password']
                    user_obj.name = request.data['name']
                    user_obj.save()
                    access_token = AccessToken().for_user(user_obj)
                    refresh_token = RefreshToken().for_user(user_obj)
                    return Response({
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                        "phone": str(user_obj.phone),
                        "name": str(user_obj.name),
                        "password": str(user_obj.password)
                    })

        except:
            return Response({
                "status": False,
                "detail": "Siz bir martalik mahfiy kodni kiritmgansiz. Shuning uchun ro'yhatdan o'ta olmaysiz!"
            })

class RegisterViewCredit(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=Register, tags=['Register'])
    def post(self, request):
        serializer1 = Register(data=request.data)
        serializer2 = Credit(data=request.data)

        if serializer1.is_valid() and serializer2.is_valid():
            try:
                verify = ValidatedOtp.objects.filter(phone__iexact=request.data['phone'], validated=True)
                if verify.exists():
                    user_data = serializer1.validated_data
                    user_data['password'] = make_password(user_data['password'])
                    user_obj = User.objects.create(**user_data)

                    credit_data = serializer2.validated_data
                    credit_obj = Userdata.objects.create(user=user_obj, **credit_data)

                    access_token = AccessToken().for_user(user_obj)
                    refresh_token = RefreshToken().for_user(user_obj)

                    return Response({
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                        "phone": user_obj.phone,
                        "name": user_obj.name,
                    })

            except Exception as e:
                print(str(e))
                return Response({
                    "status": False,
                    "detail": "Siz bir martalik mahfiy kodni kiritmgansiz. Shuning uchun ro'yhatdan o'ta olmaysiz!"
                }, status=400)

        else:
            return Response({
                "user_errors": serializer1.errors,
                "credit_errors": serializer2.errors
            }, status=400)

class CreditView(APIView):
    def post(self, request, id):
        user = User.objects.filter(id = id).first()
        if user:
            serializer = Credit(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response('Bunday user yoq')

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Log

    @swagger_auto_schema(request_body=Log)
    def post(self, request):
        try:
            print("try")
            user = User.objects.get(phone=request.data['phone'])

            if check_password(request.data['password'], user.password):
                print('if')
                phone = User.objects.get(phone=request.data['phone'])
                access_token = AccessToken().for_user(phone)
                refresh_token = RefreshToken().for_user(phone)
                return Response({
                    "id": phone.id,
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                })
            else:
                print('else')
                return Response({'Xato': "Noto'g'ri password kiritdingiz :("})

        except:
            print('except')
            return Response({'Xato': 'Bunday user mavjud emas :('})


class UserAccView(APIView):

    def get(self, request, *args, **kwargs):
        userdata = Userdata.objects.all()
        serializer = Accaunt(userdata, many=True)
        return Response(serializer.data)


class UserdataUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Userdata'])
    def get(self, request, pk):
        try:
            userdata = Userdata.objects.get(pk=pk)
        except Userdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = Accaunt(userdata)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=Accaunt, tags=['Userdata'])
    def patch(self, request, pk):
        try:
            userdata = Userdata.objects.get(pk=pk)
        except Userdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = Accaunt(instance=userdata, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Userdata'])
    def delete(self, request, pk):
        try:
            userdata = Userdata.objects.get(pk=pk)
        except Userdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = userdata.user
        userdata.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    my_tags = ['Change-Password']

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Password successfully updated'}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView): # tel o'zgartirilgandagi verificatsiya
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]
    queryset = Verification.objects.all()

    @swagger_auto_schema(request_body=VerifyCodeSerializer, tags=['Password-Reset'])
    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            obj = Verification.objects.get(phone=data['phone'])
            serializer = VerifyCodeSerializer(instance=obj, data=data)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['step_change_phone'] == 'confirmed':
                    user = request.user
                    user.phone = data['phone']
                    user.save()
                    return Response({'message': 'Your phone number has been successfully changed!'},
                                status=status.HTTP_202_ACCEPTED)
                return Response({'message': 'This phone number has been successfully verified!'},
                                status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Verification.DoesNotExist:
            return Response({'error': 'Phone number or verify code incorrect!'}, statusis_pupil=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneSRL
    my_tags = ['Password-Reset']

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Password-Reset'])
    def post(self, request):
        data = request.data
        if data.get('phone'):
            phone = data['phone']
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                user = user.first()
                context = send_sms(phone)
                return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
            return Response({'msg': _('User not found!')})
        return Response({'msg': _("Enter phone number")}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordVerifyCode(VerifyCodeView):
    my_tags = ['Password-Reset']

class ResetPasswordConfirm(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(request_body=ResetPasswordSerializer, tags=['Password-Reset'])
    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            return Response({'error': "User matching query doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            ver = Verification.objects.get(phone=request.data['phone'])
            print('Ver', ver.step_reset)
            user.set_password(request.data['new_password'])
            ver.step_reset = ''
            ver.save()
            user.save()
            return Response({'message': 'Password successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePhoneNumber(APIView):
    queryset = User.objects.all()
    serializer_class = PhoneSRL
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Account'])
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone")
        if phone_number.isdigit() and len(phone_number) > 8:
            user = User.objects.filter(phone__iexact=phone_number)
            if user.exists():
                return Response({
                    "status": False,
                    "detail": "Bu raqam avval registerdan otgan."
                })
            else:
                otp = send_sms(phone_number)
                if 'verify_code' in otp:
                    code = str(otp['verify_code'])
                    try:
                        validate = ValidatedOtp.objects.get(phone=phone_number)
                        if validate.validated:
                            validate.otp = code
                            validate.validated = False
                            validate.save()
                        else:
                            pass

                    except ValidatedOtp.DoesNotExist as e:
                        phon = ValidatedOtp.objects.filter(phone__iexact=phone_number)
                        if not phon.exists():
                            ValidatedOtp.objects.create(phone=phone_number, otp=code, validated=False)
                        else:
                            Response({"phone": "mavjud"})

                return Response({
                    "status": True,
                    "detail": "SMS xabarnoma jo'natildi",
                    "code": otp  # <--vaqtinchalik qo'shildi
                })
        else:
            if len(phone_number) < 8:
                return Response({"detail": "Telefon raqamingizni kod bilan kiriting!"})
            else:
                return Response({
                    "status": False,
                    "detail": "Telefon raqamni kiriting ."
                })


class ChangePhoneNumberVerifyCode(APIView):
    my_tags = ['Account']
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]
    queryset = Verification.objects.all()

    @swagger_auto_schema(request_body=VerifyCodeSerializer, tags=['Account'])
    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            obj = Verification.objects.get(phone=data['phone'])
            serializer = VerifyCodeSerializer(instance=obj, data=data)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['step_change_phone'] == 'confirmed':
                    user = request.user
                    user.phone = data['phone']
                    user.save()
                    return Response({'message': 'Your phone number has been successfully changed!'},
                                    status=status.HTTP_202_ACCEPTED)
                return Response({'message': 'This phone number has been successfully verified!'},
                                status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Verification.DoesNotExist:
            return Response({'error': 'Phone number or verify code incorrect!'},
                            statusis_pupil=status.HTTP_400_BAD_REQUEST)



class ChangePhoneNumberConfirm(APIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneSRL

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Account'])
    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone=request.user)
        except:
            return Response({'error': "User matching query doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhoneSRL(instance=user, data=request.data)
        if serializer.is_valid():
            ver = Verification.objects.get(phone=request.data['phone'])
            user.phone = request.data['phone']
            user.save()
            ver.step_reset = ''
            ver.delete()

            updated_user = User.objects.get(phone=serializer.data['phone'])
            access_token = AccessToken().for_user(updated_user)
            refresh_token = RefreshToken().for_user(updated_user)

            return Response({'message': 'Phone successfully updated',
                             'access': str(access_token),
                             'refresh': str(refresh_token),
                             })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



