from django.urls import path
from .views import (
    ExpenseListCreateAPIView, 
    ExpenseDetailAPIView,
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    CategorySpendLimitAPIView
    )

urlpatterns = [
    path('expenses/', ExpenseListCreateAPIView.as_view()),
    path('expenses/<slug>/', ExpenseDetailAPIView.as_view()),

    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<slug>/', CategoryDetailAPIView.as_view()),
    path('categories/<slug>/set-limit/', CategorySpendLimitAPIView.as_view())

]