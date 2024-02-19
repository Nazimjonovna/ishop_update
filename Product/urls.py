from django.urls import path
from .views import *

urlpatterns = [
    path('add_category/<int:id>/', CreateCategoryView.as_view()), # Categpry qo'shish id - adminniki
    path('ass_subcategory/<int:id>/', CreateSubCategoryView.as_view()), # SubCategpry qo'shish id - adminniki
    path('add_product/', AddProdcutView.as_view()),
]