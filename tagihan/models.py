import moneyed
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import Permission, User
from django.db import models

class Anggaran(models.Model):
    user = models.ManyToManyField(User, default=1)
    money_amount = models.DecimalField(max_digits=13, decimal_places=0)
    amount_date = models.DateField()

    class Meta:
        ordering = ["amount_date"]

    def __str__(self):
        return str(self.amount_date)

class Pembayaran(models.Model):
    anggaran = models.ForeignKey(Anggaran, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=500)
    vendor_number = models.CharField(max_length=50)
    bill_number = models.CharField(max_length=250)
    receipt_number = models.CharField(max_length=250)
    employee_payment = models.DecimalField(max_digits=13, decimal_places=0, null=True, blank=True)
    pension_payment = models.DecimalField(max_digits=13, decimal_places=0, null=True, blank=True)
    payment_date = models.DateField()
    is_verified = models.BooleanField(default=False)
    is_problem = models.CharField(max_length=500, null=True, blank=True, default='Tidak Ada')
    verification_date = models.DateField(null=True, blank=True)

    class Meta:
        permissions = (
            ("change_is_verified", "Can edit verification"),
            ("fill_is_problem", "Can fill problem form"),
            ("view_is_verified", "Can view verification"),
            ("view_is_problem", "Can view problem"),
            ("print_output", "Can Print Report"),
            ("can_login", "Can Login to Index"),
            ("is_administration", "User is Administration"),
            ("is_keuangan","User is Keuangan"),
        )

    def __str__(self):
        return self.provider_name + ' / ' + self.vendor_number + ' / ' + str(self.payment_date)
