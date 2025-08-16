from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import SubAccount, Category, Transaction
from django.db import transaction
from django.db.models.signals import post_delete


# When a new user signs up, this function automatically creates two sub-accounts for the new user using the SubAccount class from the model:
# One for tracking income
# One for tracking expenses
# Creates predefined categories for the expense account

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_sub_accounts_and_categories(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            income_account, _ = SubAccount.objects.get_or_create(
                user=instance, 
                account_type="income",
                defaults={"balance": 0.00}
            )

            expense_account, _ = SubAccount.objects.get_or_create(
                user=instance, 
                account_type="expense",
                defaults={"balance": 0.00}
            )

            predefined_categories = [
                "Food","Transportation", "Rent", "Utilities", "Entertainment",
                "Healthcare", "Education", "Clothing", "Personal Care", "Savings","Other"
            ]

            for cat in predefined_categories:
                Category.objects.get_or_create(sub_account=expense_account, name=cat)



# This function updates the account balance when a transaction is deleted
@receiver(post_delete, sender=Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    account = instance.account

    if instance.transaction_type == "income":
        account.balance -= instance.amount
    elif instance.transaction_type == "expense":
        account.balance += instance.amount

    account.save()