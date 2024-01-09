from django.db import models
from django.contrib.auth.models import User
from categories.models import CategoriesModel

# Create your models here.


class BooksModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="books/media/uploads",
        height_field=None,
        width_field=None,
        max_length=None,
        default="",
    )

    def __str__(self):
        return self.title


class ReviewModel(models.Model):
    post = models.ForeignKey(
        BooksModel, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PurchaseHistoryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(BooksModel, on_delete=models.CASCADE)
    borrowed = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} borrowed: {self.book.title}"
