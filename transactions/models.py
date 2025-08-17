from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import transaction

# Create your models here.

class SubAccount(models.Model):
    ACCOUNT_TYPES = [
        ("income", "Income"),
        ("expense", "Expense")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"
    




class Category(models.Model):
    sub_account = models.ForeignKey(SubAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name




class Transaction(models.Model):
    sub_account = models.ForeignKey(SubAccount, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_amount = 0

        if not is_new:
            old_amount = Transaction.objects.get(pk=self.pk).amount

        super().save(*args, **kwargs)

        with transaction.atomic():
            if self.sub_account.account_type == "income":
                if is_new:
                    self.sub_account.balance += self.amount
                else:
                    self.sub_account.balance += (self.amount - old_amount)
            elif self.sub_account.account_type == "expense":
                if is_new:
                    self.sub_account.balance -= self.amount
                else:
                    self.sub_account.balance -= (self.amount - old_amount)
            
            self.sub_account.save()

    def __str__(self):
        return f"{self.sub_account.account_type} - {self.amount}"