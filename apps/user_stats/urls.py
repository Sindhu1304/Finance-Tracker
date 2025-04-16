from django.urls import path 

from .views import ExpensesStats

urlpatterns = [
    path('expense-stats/', ExpensesStats.as_view()),
]