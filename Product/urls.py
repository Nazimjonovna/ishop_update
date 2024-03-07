from django.urls import path
from .views import *

urlpatterns = [
    path('add_category/<int:id>/', CreateCategoryView.as_view()), # Categpry qo'shish id - adminniki
    path('ass_subcategory/<int:id>/', CreateSubCategoryView.as_view()), # SubCategpry qo'shish id - adminniki
    path('add_product/', AddProdcutView.as_view()),
    path("edit_product/<int:id>/", EditProduct.as_view()),
    path("get_producst/", GetProductView.as_view()),
    path('post_order/<int:id>/', PostOrderView.as_view()),
    path("get_orders/<int:id>/", GetOrderView.as_view()),
    path('get_order/<int:id>/', GetOneOrderView.as_view()),
    path('edit_order/<int:id>/', OrderEditView.as_view()),
    path('backet/<int:id>/', BasketView.as_view()),
    path('get_likde_orders/<int:id>/', GetLikedOrdersView.as_view()),
    
]