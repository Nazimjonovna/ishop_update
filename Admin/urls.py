from django.urls import path
from .views import *

urlpatterns = [
    path('Add_admin/<int:id>/', AddAdminView.as_view()),
    path('login_admin/<int:id>/', LoginAdminview.as_view()),
    path('add_protsent/', AddProtsent.as_view()),
    path('change_tasdiq/<int:id>/', EditTasdiqView.as_view()),
    path('get_son/<int:id>/', GetSonProduct.as_view()),
    path('get_admin/<int:id>', GetAdminsView.as_view()),
    path('chek_admin/<int:pk>/', AdminChekView.about_view()),
]