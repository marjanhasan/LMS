from django.contrib import admin

# from .views import send_transaction_email
# from transactions.models import Transaction
from .models import TransactionsModel


@admin.register(TransactionsModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "amount",
    ]

    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.account.save()
        super().save_model(request, obj, form, change)
