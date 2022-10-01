from django.contrib.auth.models import User
from django.db import models
#from contribution.models import Cust_contrb

class Customer(models.Model):
	user = models.OneToOneField(User, related_name='Customer', on_delete=models.CASCADE)
	#cust_contrb = models.ForeignKey(Cust_contrb, related_name='Customer', on_delete=models.CASCADE)
	name = models.CharField(max_length=45)
	gender = models.CharField(max_length=6, blank=True)
	tel = models.CharField(max_length=12, blank=True)
	branch = models.CharField(max_length=50, blank=True)
	payment_plan = models.CharField(max_length=50, blank=True)
	package = models.CharField(max_length=50, blank=True)
	business_addr = models.CharField(max_length=150, blank=True, null=True)
	home_addr = models.CharField(max_length=150, blank=True)
	acct_bank = models.CharField(max_length=50, blank=True, null=True)
	acct_name = models.CharField(max_length=100, blank=True, null=True)
	acct_no = models.CharField(max_length=15, blank=True, null=True)
	kin_name = models.CharField(max_length=45, blank=True)
	kin_tel = models.CharField(max_length=15, blank=True)
	kin_relationship = models.CharField(max_length=15, blank=True)
	created_by = models.CharField(max_length=100, blank=True, null=True)

User.customerprofile = property(lambda u:Customer.objects.get_or_create(user=u)[0])
#Cust_contrb.cust_contrbprofile = property(lambda u:Cust_contrb.objects.get_or_create(user=u)[0])

class Teller(models.Model):
	user = models.OneToOneField(User, related_name='Teller', on_delete=models.CASCADE)
	name = models.CharField(max_length=45)
	gender = models.CharField(max_length=6, blank=True)
	tel = models.CharField(max_length=12, blank=True)
	home_addr = models.CharField(max_length=150, blank=True)
	acct_bank = models.CharField(max_length=50, blank=True, null=True)
	acct_name = models.CharField(max_length=100, blank=True, null=True)
	acct_no = models.CharField(max_length=15, blank=True, null=True)
	kin_name = models.CharField(max_length=45, blank=True)
	kin_tel = models.CharField(max_length=15, blank=True)
	kin_relationship = models.CharField(max_length=15, blank=True)
	created_by = models.CharField(max_length=100, blank=True, null=True)

User.tellerprofile = property(lambda u:Teller.objects.get_or_create(user=u)[0])


class Manager(models.Model):
	user = models.OneToOneField(User, related_name='Manager', on_delete=models.CASCADE)
	name = models.CharField(max_length=45)
	gender = models.CharField(max_length=6, blank=True)
	tel = models.CharField(max_length=12, blank=True)
	home_addr = models.CharField(max_length=150, blank=True)
	acct_bank = models.CharField(max_length=50, blank=True, null=True)
	acct_name = models.CharField(max_length=100, blank=True, null=True)
	acct_no = models.CharField(max_length=15, blank=True, null=True)
	kin_name = models.CharField(max_length=45, blank=True)
	kin_tel = models.CharField(max_length=15, blank=True)
	kin_relationship = models.CharField(max_length=15, blank=True)
	created_by = models.CharField(max_length=100, blank=True, null=True)

User.managerprofile = property(lambda u:Manager.objects.get_or_create(user=u)[0])