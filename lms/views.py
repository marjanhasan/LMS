from django.shortcuts import render
from books.models import BooksModel
from categories.models import CategoriesModel


def home(request, category=None):
    data = BooksModel.objects.all()
    if category is not None:
        name = CategoriesModel.objects.get(slug=category)
        data = BooksModel.objects.filter(category=name)
    books = CategoriesModel.objects.all()
    return render(request, "home.html", {"data": data, "books": books})
