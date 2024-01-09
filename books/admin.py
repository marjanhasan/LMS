from django.contrib import admin
from .models import BooksModel, ReviewModel, PurchaseHistoryModel

# Register your models here.
admin.site.register(BooksModel)
admin.site.register(ReviewModel)
admin.site.register(PurchaseHistoryModel)
