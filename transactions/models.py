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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"