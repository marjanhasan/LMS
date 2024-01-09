from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from transactions.forms import DepositForm
from transactions.models import TransactionsModel
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_transaction_email(user, amount, subject, template):
    message = render_to_string(
        template,
        {
            "user": user,
            "amount": amount,
        },
    )
    send_email = EmailMultiAlternatives(subject, "", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = "transaction_form.html"
    model = TransactionsModel
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"account": self.request.user.account})
        return kwargs


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        account = self.request.user.account

        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()

        account.balance += amount
        account.save(update_fields=["balance"])

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited successfully',
        )
        send_transaction_email(
            self.request.user, amount, "Deposite message", "deposite.html"
        )

        return super().form_valid(form)
