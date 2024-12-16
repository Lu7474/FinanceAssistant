from django.urls import path

from .views import index, category_view, category_add, expense_add, expense_view, income_add, income_view

urlpatterns = [
    path("", index, name="base"),
    path("categories", category_view, name="category_view"),
    path("categories/add", category_add, name="add_category"),
    path("expenses", expense_view, name="expense_view"),
    path("expenses/add", expense_add, name="add_expense"),
    path("income", income_view, name="income_view"),
    path("income/add", income_add, name="add_income"),
]
