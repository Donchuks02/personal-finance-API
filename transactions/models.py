from django.db import models
from django.conf import settings

# Create your models here.


class Transaction(models.Model):

    INCOME = "IN"
    EXPENSE = "EX"

    TRANSACTION_TYPES =[
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    CATEGORY_CHOICES = [
        ('food_groceries', 'Food & Groceries'),
        ('transportation', 'Transportation'),
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('internet_phone', 'Internet & Phone'),
        ('entertainment', 'Entertainment'),
        ('health_medical', 'Health & Medical'),
        ('clothing', 'Clothing'),
        ('education', 'Education'),
        ('savings', 'Savings'),
        ('gifts_donations', 'Gifts & Donations'),
        ('personal_care', 'Personal Care'),
        ('travel', 'Travel'),
        ('home_maintenance', 'Home Maintenance'),
        ('childcare', 'Childcare'),
        ('insurance', 'Insurance'),
        ('salary', 'Salary'),
        ('investment_income', 'Investment Income'),
        ('other', 'Other'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    # category = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"