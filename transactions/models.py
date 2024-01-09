from django.db import models
from user.models import UserModel

# Create your models here.


class TransactionsModel(models.Model):
    account = models.ForeignKey(
        UserModel, related_name="transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
