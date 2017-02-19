from django import forms
from django.contrib.auth.models import User
from .models import Anggaran, Pembayaran
from functools import partial

DateInput = partial(forms.DateInput, {'class':'datepicker'})

class AnggaranForm(forms.ModelForm):
    amount_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Anggaran
        fields = ['money_amount', 'amount_date']


class PembayaranForm(forms.ModelForm):
    payment_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Pembayaran
        fields = [
        'provider_name', 'vendor_number', 'bill_number', 'receipt_number', 'employee_payment',
        'pension_payment', 'payment_date'
        ]

class ProblemForm(forms.ModelForm):
    verification_date = forms.DateField(widget=DateInput())
    is_problem = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Pembayaran
        fields = [
            'is_problem', 'verification_date'
        ]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
