from django.shortcuts import render, redirect
from .models import Category, Expense, Income


def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    context = {
        "categories": categories,
        "expenses": expenses,
        "incomes": incomes,
    }
    return render(request, "index.html", context)


def category_view(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {"categories": categories})


def category_add(request):
    if request.POST:
        title = request.POST.get("title")
        if title:
            Category.objects.create(title=title)
            return redirect("category_view")

    return render(request, "add_category.html")


def expense_view(request):
    expenses = Expense.objects.all()
    return render(request, "expenses.html", {"expenses": expenses})


def expense_add(request):
    if request.POST:
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        if amount and category_id:
            category = Category.objects.get(id=category_id)
            Expense.objects.create(amount=amount, category=category)
            return redirect("expense_view")

    categories = Category.objects.all()
    return render(request, "add_expense.html", {"categories": categories})


def income_view(request):
    incomes = Income.objects.all()
    return render(request, "income.html", {"incomes": incomes})


def income_add(request):
    if request.POST:
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        if amount and category_id:
            category = Category.objects.get(id=category_id)
            Income.objects.create(amount=amount, category=category)
            return redirect("income_view")

    categories = Category.objects.all()
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
