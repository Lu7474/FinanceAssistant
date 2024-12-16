from django.shortcuts import render, redirect
from .models import Category, Expense, Income


def index(request):
    context = {}
    return render(request, "base.html", context)


def category_view(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {"categories": categories})


def category_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Category.objects.create(title=title)
            return redirect("category_view")

    return render(request, "add_category.html")


def expense_view(request):
    expenses = Expense.objects.all()
    return render(request, "expenses.html", {"expenses": expenses})


def expense_add(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        date = request.POST.get("date")
        if amount and category_id and date:
            category = Category.objects.get(id=category_id)
            Expense.objects.create(amount=amount, category=category, date=date)
            return redirect("expense_view")

    categories = Category.objects.all()
    return render(request, "add_expense.html", {"categories": categories})


def income_view(request):
    incomes = Income.objects.all()
    return render(request, "income.html", {"incomes": incomes})


def income_add(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        date = request.POST.get("date")
        if amount and category_id and date:
            category = Category.objects.get(id=category_id)
            Income.objects.create(amount=amount, category=category, date=date)
            return redirect("income_view")

    categories = Category.objects.all()
    return render(request, "add_income.html", {"categories": categories})
