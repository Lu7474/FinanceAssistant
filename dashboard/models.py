from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор категории",
    )

    def __str__(self):
        return self.title


class Expense(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name="Категория",
    )
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор расхода",
    )

    def __str__(self):
        return f"{self.amount} - {self.category.title}"


class Income(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="incomes",
        verbose_name="Категория",
    )
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор дохода",
    )
    
    def __str__(self):
        return f"{self.amount} - {self.category.title}"
