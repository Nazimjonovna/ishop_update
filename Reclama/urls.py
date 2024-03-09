from django.urls import path
from .views import *

urlpatterns = [
    path('add_advertising/<int:id>/', AddReclamaView.as_view()),
    path('get_advertisings/', GetReclamaView.as_view()),
    path('add_category_advertising/<int:id>/', AddCategoryRecView.as_view()),
    path('get_category_advertising/', GetCategoryRecView.as_view()),
    path('add_card_advertising/<int:id>/', AddRecCardView.as_view()),
    path('get_card_advertising/', GetRecCardView.as_view()),
]