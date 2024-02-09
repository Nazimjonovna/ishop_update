from django.urls import path
from .views import *

urlpatterns = [
    path('phone/', PhoneView.as_view()),
    path('otp/', OtpView.as_view()),
    path('register/naqt/', RegisterViewNaqt.as_view()),
    path('register/credit2/<int:id>/', CreditView.as_view()),
    path('register/credit/', RegisterViewCredit.as_view()),
    path('login/', LoginView.as_view()),
    path('get/', UserAccView.as_view()),
    path('acc/<int:pk>/', UserdataUpdateDeleteView.as_view()),
    path('ch_pass/<int:pk>/', ChangePasswordView.as_view()),
    path('resent', ResetPasswordView.as_view()),
    path('resent_code/', ResetPasswordVerifyCode.as_view()),
    path('resent_confirm/', ResetPasswordConfirm.as_view()),
    path('ch_phone/', ChangePhoneNumber.as_view()),
    path('ch_phone_verify/', ChangePhoneNumberVerifyCode.as_view()),
    path('ch_phone_conf/', ChangePhoneNumberConfirm.as_view()),
]


