from django.contrib.auth.models import User
from django.db import models
from customer.models import Customer

class Contribution(models.Model):
	customer = models.ForeignKey(Customer, related_name='contribution', on_delete=models.CASCADE)
	contribution_day = models.CharField(max_length=2)
	contribution_month = models.CharField(max_length=12)
	contribution_year = models.CharField(max_length=4)
	amount_paid = models.CharField(max_length=15, blank=True, null=True)
	transaction = models.CharField(max_length=50)
	payment_plan = models.CharField(max_length=15, blank=True, null=True)
	recorded_by = models.CharField(max_length=30, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Cust_contrb(models.Model):
	customer = models.OneToOneField(Customer, related_name='cust_contrb', on_delete=models.CASCADE)
	duration = models.CharField(max_length=15, default=0)
	charges = models.CharField(max_length=15, default=0)
	total = models.CharField(max_length=15, default=0)
	wallet = models.CharField(max_length=15, default=0)
	contribution_period = models.CharField(max_length=20, default=0)
	set_current_contrib_period = models.CharField(max_length=20, default=0)
	deducted_commission_for = models.CharField(max_length=35, default=0)

Cust_contrb.customerprofile = property(lambda u:Customer.objects.get_or_create(customer=u)[0])

#Customer.contributionprofile = property(lambda u:Contribution.objects.get_or_create(customer=u)[0])
#User.customerprofile = property(lambda u:Customer.objects.get_or_create(user=u)[0])

class Account(models.Model):
	date_charged = models.CharField(max_length=45)
	contribution_month = models.CharField(max_length=12, blank=True)
	contribution_year = models.CharField(max_length=4, blank=True)

#Cust_contrb.account = property(lambda u:Customer.objects.get_or_create(customer=u)[0])

class Withdrawal(models.Model):
	customer = models.ForeignKey(Customer, related_name='withdrawal', on_delete=models.CASCADE)
	amount = models.CharField(max_length=15, blank=True, null=True)
	withdrawal_date = models.CharField(max_length=15, blank=True, null=True)
	recorded_by = models.CharField(max_length=30, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
