from django.urls import path
from .views import *

urlpatterns = [
    path('post_partner/<int:id>/', PostPartnerView.as_view()),
    path('get_partners/<int:id>/', GetPartnerView.as_view()),
    path('edit_partner/<int:id>/', EditPartnerView.as_view()),
]