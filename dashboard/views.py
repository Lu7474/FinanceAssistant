from django.views.generic import DetailView
from django.shortcuts import render, redirect
from .models import Category, Expense, Income
from django.db.models import Sum


def index(request):
    if not request.user.is_authenticated:
        return redirect("users/login/")
    categories = Category.objects.filter(author=request.user)
    expenses = Expense.objects.filter(author=request.user)
    incomes = Income.objects.filter(author=request.user)
    sum_inc = Income.objects.filter(author=request.user).aggregate(
        total_inc=Sum("amount")
    )
    total_inc = sum_inc["total_inc"] or 0
    sum_exp = Expense.objects.filter(author=request.user).aggregate(
        total_exp=Sum("amount")
    )
    total_exp = sum_exp["total_exp"] or 0
    context = {
        "categories": categories,
        "expenses": expenses,
        "incomes": incomes,
        "total_exp": total_exp,
        "total_inc": total_inc,
    }
    return render(request, "index.html", context)


def category_view(request):
    categories = Category.objects.filter(author=request.user)
    return render(request, "categories.html", {"categories": categories})


def category_add(request):
    if request.POST:
        title = request.POST.get("title")
        if title:
            Category.objects.create(title=title, author=request.user)
            return redirect("category_view")

    return render(request, "add_category.html")


def expense_view(request):
    expenses = Expense.objects.filter(author=request.user)
    sum_exp = Expense.objects.filter(author=request.user).aggregate(
        total_exp=Sum("amount")
    )
    total_exp = sum_exp["total_exp"] or 0
    context = {
        "expenses": expenses,
        "total_exp": total_exp,
    }
    return render(request, "expenses.html", context)


def expense_add(request):
    if request.POST:
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        if amount and category_id:
            category = Category.objects.get(id=category_id)
            Expense.objects.create(
                amount=amount, category=category, author=request.user
            )
            return redirect("expense_view")

    categories = Category.objects.filter(author=request.user)
    return render(request, "add_expense.html", {"categories": categories})


def income_view(request):
    incomes = Income.objects.filter(author=request.user)
    sum_inc = Income.objects.filter(author=request.user).aggregate(
        total_inc=Sum("amount")
    )
    total_inc = sum_inc["total_inc"] or 0
    context = {
        "incomes": incomes,
        "total_inc": total_inc,
    }
    return render(request, "income.html", context)


def income_add(request):
    if request.POST:
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        if amount and category_id:
            category = Category.objects.get(id=category_id)
            Income.objects.create(amount=amount, category=category, author=request.user)
            return redirect("income_view")

    categories = Category.objects.filter(author=request.user)
    return render(request, "add_income.html", {"categories": categories})


def category_del(request, id=None):
    if id and request.POST:
        Category.objects.filter(id=id).delete()
    return redirect("category_view")


def expense_del(request, id=None):
    if id and request.POST:
        Expense.objects.filter(id=id).delete()
    return redirect("expense_view")


def income_del(request, id=None):
    if id and request.POST:
        Income.objects.filter(id=id).delete()
    return redirect("income_view")


class CategoryDetailView(DetailView):
    model = Category
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.object
        user = self.request.user

        sum_exp = Expense.objects.filter(category=category, author=user).aggregate(
            total_exp=Sum("amount")
        )
        total_exp = sum_exp["total_exp"] or 0

        sum_inc = Income.objects.filter(category=category, author=user).aggregate(
            total_inc=Sum("amount")
        )
        total_inc = sum_inc["total_inc"] or 0

        category = self.object
        context["expenses"] = Expense.objects.filter(category=category, author=user)
        context["total_exp"] = total_exp
        context["incomes"] = Income.objects.filter(category=category, author=user)
        context["total_inc"] = total_inc

        return context
