from django.shortcuts import render, redirect
from books.models import BooksModel, ReviewModel, PurchaseHistoryModel
from books.forms import ReviewForm
from user.models import UserModel
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# Create your views here.
def send_transaction_email(user, subject, template):
    message = render_to_string(template, {"user": user})
    send_email = EmailMultiAlternatives(subject, "", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


def details_view(request, id):
    books = BooksModel.objects.get(pk=id)
    comments = ReviewModel.objects.all()

    if request.method == "POST":
        comment_form = ReviewForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = books
            comment.save()
    else:
        comment_form = ReviewForm()
    if request.user.is_authenticated:
        borrowed = PurchaseHistoryModel.objects.filter(
            user=request.user, book=books, borrowed=True
        ).exists()
        return render(
            request,
            "details.html",
            {
                "book": books,
                "comment_form": comment_form,
                "comments": comments,
                "borrowed": borrowed,
            },
        )
    else:
        return render(request, "details.html", {"book": books})


def borrow_view(request, id, userid):
    userid -= 1
    data = BooksModel.objects.get(pk=id)
    account = UserModel.objects.get(pk=userid)
    quantity = data.quantity
    price = data.price
    balance = account.balance
    purchase_history = False

    if balance > price and quantity > 1:
        quantity -= 1
        balance -= price
        account.balance = balance

        data.quantity = quantity
        data.save()

        purchase_history = PurchaseHistoryModel.objects.create(
            user=request.user, book=data
        )
        account.save()

        messages.success(request, f"Successfully borrowed a book")

        send_transaction_email(
            request.user, "Book borrowed successful", "borrow_success.html"
        )
        return redirect("profile")
    else:
        messages.warning(
            request,
            f"Not have enough balance",
        )
        send_transaction_email(
            request.user, "Book borrowed failed", "borrow_failed.html"
        )

    return render(request, "details.html", {"book": data, "borrowed": purchase_history})


def return_view(request, id, userid, buyid):
    userid -= 1
    data = BooksModel.objects.get(pk=id)
    account = UserModel.objects.get(pk=userid)
    quantity = data.quantity
    price = data.price
    balance = account.balance
    if balance > price:
        if quantity > 1:
            quantity += 1
            balance += price
            account.balance = balance
            data.quantity = quantity
            account.save()
            data.save()
            deleteHistory = PurchaseHistoryModel.objects.get(id=buyid)
            deleteHistory.delete()
            send_transaction_email(
                request.user, "Book returned successfull", "return_success.html"
            )
            return redirect("profile")
    else:
        messages.warning(
            request,
            f"Not have enough balance",
        )
        send_transaction_email(
            request.user, "Book returned failed", "return_failed.html"
        )
    return render(request, "details.html", {"book": data})
