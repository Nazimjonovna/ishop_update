from django.urls import path
from .views import *

urlpatterns = [
    path('phone/', PhoneView.as_view()),
    path('one_time_sms_check/', OtpView.as_view()),
    path('register/', RegisterViewNaqt.as_view()),
    path('register_addtition/<int:id>/', CreditView.as_view()),
    path('login/', LoginView.as_view()),
    path('get_user/', UserAccView.as_view()),
    path('get_user_data/<int:pk>/', UserdataUpdateDeleteView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view()),
    path('resent_password', ResetPasswordView.as_view()),
    path('resent_password_verify/', ResetPasswordVerifyCode.as_view()),
    path('resent_password_confirm/', ResetPasswordConfirm.as_view()),
    path('change_phone/', ChangePhoneNumber.as_view()),
    path('change_phone_verify/', ChangePhoneNumberVerifyCode.as_view()),
    path('change_phone_confirm/', ChangePhoneNumberConfirm.as_view()),
]


