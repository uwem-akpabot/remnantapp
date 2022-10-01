from django.db import models

#COMPANY'S MONEY
class Company_account(models.Model):
    transaction_type = models.CharField(max_length=12) #e.g. deposit, withdrawal
    transaction_detail = models.CharField(max_length=100) #e.g. June 2022 month charge on John Doe
    amount = models.CharField(max_length=12, default=0)
    curr_balance = models.CharField(max_length=45, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#NOT COMPANY'S MONEY, money will be used to payback customers - Account balance of customers contribution
class Contribution_account(models.Model):
    contrib_acct_transaction_type = models.CharField(max_length=12) #e.g. deposit, withdrawal
    contrib_acct_transaction_detail = models.CharField(max_length=100) #e.g. June 2022 month charge on John Doe
    contrib_acct_amount = models.CharField(max_length=12, blank=True)
    contrib_acct_curr_balance = models.CharField(max_length=45, default=0)
    contrib_acct_created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Admin_total_funds(models.Model):
    balance = models.CharField(max_length=12, default=0) 
