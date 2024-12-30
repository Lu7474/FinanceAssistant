from django.views.generic import DetailView
from django.http import HttpResponseServerError
from django.db import DatabaseError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Expense, Income
from django.db.models import Sum


def user_registered(func):
    def registered(request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return redirect("/users/login/")
            return func(request, *args, **kwargs)
        except AttributeError:
            return HttpResponseServerError("Ошибка: пользователь не определен.")

    return registered


def get_totals(user, model, filter_params=None):
    try:
        filter_params = filter_params or {}
        items = model.objects.filter(author=user, **filter_params)
        total = items.aggregate(total=Sum("amount")).get("total", 0)
        return items, total
    except DatabaseError as e:
        print(f"Database error: {e}")
        return None, 0


@user_registered
def index(request):
    categories = Category.objects.filter(author=request.user).select_related("author")
    expenses, total_exp = get_totals(request.user, Expense)
    incomes, total_inc = get_totals(request.user, Income)
    context = {
        "categories": categories,
        "expenses": expenses,
        "incomes": incomes,
        "total_exp": total_exp,
        "total_inc": total_inc,
    }
    return render(request, "index.html", context)


@user_registered
def category_view(request):
    categories = Category.objects.filter(author=request.user).select_related("author")
    return render(request, "categories.html", {"categories": categories})


@user_registered
def category_add(request):
    if request.POST:
        title = request.POST.get("title")
        if title:
            Category.objects.create(title=title, author=request.user)
            return redirect("category_view")
    return render(request, "add_category.html")


@user_registered
def expense_view(request):
    expenses, total_exp = get_totals(request.user, Expense)
    context = {"expenses": expenses, "total_exp": total_exp}
    return render(request, "expenses.html", context)


@user_registered
def expense_add(request):
    if request.POST:
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        if amount and category_id:
            category = get_object_or_404(Category, id=category_id)
            Expense.objects.create(
                amount=amount, category=category, author=request.user
            )
            return redirect("expense_view")

    categories = Category.objects.filter(author=request.user).select_related("author")
    return render(request, "add_expense.html", {"categories": categories})


@user_registered
def income_view(request):
    incomes, total_inc = get_totals(request.user, Income)
    context = {"incomes": incomes, "total_inc": total_inc}
    return render(request, "income.html", context)


@user_registered
def income_add(request):
    if request.POST:
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        if amount and category_id:
            category = get_object_or_404(Category, id=category_id)
            Income.objects.create(amount=amount, category=category, author=request.user)
            return redirect("income_view")

    categories = Category.objects.filter(author=request.user).select_related("author")
    return render(request, "add_income.html", {"categories": categories})


@user_registered
def delete_item(request, model, redirect_url, id=None):
    try:
        if id and request.POST:
            model.objects.filter(id=id).delete()
        return redirect(redirect_url)
    except DatabaseError as e:
        print(f"Database error in delete_item: {e}")
        return HttpResponseServerError("Не удалось удалить запись.")


@user_registered
def category_del(request, id=None):
    return delete_item(request, Category, "category_view", id)


@user_registered
def expense_del(request, id=None):
    return delete_item(request, Expense, "expense_view", id)


@user_registered
def income_del(request, id=None):
    return delete_item(request, Income, "income_view", id)


class CategoryDetailView(DetailView):
    queryset = Category.objects.select_related("author")
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = self.object

        expenses, total_exp = get_totals(user, Expense, {"category": category})
        incomes, total_inc = get_totals(user, Income, {"category": category})
        context["expenses"] = expenses
        context["total_exp"] = total_exp
        context["incomes"] = incomes
        context["total_inc"] = total_inc

        return context
