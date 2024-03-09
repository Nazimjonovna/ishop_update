from django.urls import path
from .views import *

urlpatterns = [
    path('add_admin/<int:id>/', AddAdminView.as_view()),
    path('login/', LoginAdminview.as_view()),
    path('add_protsent/<int:id>/', AddProtsent.as_view()),
    path('edit_product_tasdiq/<int:id>/', EditTasdiqView.as_view()),
    path('get_quantity_ofProduct/<int:id>/', GetSonProduct.as_view()),
    path('order_edit_status/<int:id>/', EditOrderStatusView.as_view()),
    path('get_edit_orders/<int:id>/', GetOrderStatusView.as_view()),
    path('get_admins_work/<int:id>/', GetAdminProductsView.as_view()),
]