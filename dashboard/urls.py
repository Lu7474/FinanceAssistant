from django.urls import path

from .views import (
    index,
    category_view,
    category_add,
    expense_add,
    expense_view,
    income_add,
    income_view,
    category_del,
    expense_del,
    income_del,
    CategoryDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("categories", category_view, name="category_view"),
    path("categories/add", category_add, name="add_category"),
    path("expenses", expense_view, name="expense_view"),
    path("expenses/add", expense_add, name="add_expense"),
    path("income", income_view, name="income_view"),
    path("income/add", income_add, name="add_income"),
    path("categories/del/<int:id>", category_del, name="category_del"),
    path("expenses/del/<int:id>", expense_del, name="expense_del"),
    path("income/del/<int:id>", income_del, name="income_del"),
    path("<int:pk>", CategoryDetailView.as_view(), name="category_detail"),
]
