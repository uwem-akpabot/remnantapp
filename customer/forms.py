from django import forms
from .models import Customer, Teller, Manager

class AddCustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'gender', 'tel', 'payment_plan', 'branch', 'package', 'business_addr', 
			'home_addr', 'acct_bank', 'acct_name', 'acct_no', 'kin_name', 
			'kin_tel', 'kin_relationship'
		]

class AddTellerForm(forms.ModelForm):
	class Meta:
		model = Teller
		fields = ['name', 'gender', 'tel', 'home_addr', 'acct_bank', 'acct_name', 
			'acct_no', 'kin_name', 'kin_tel', 'kin_relationship'
		]

class AddManagerForm(forms.ModelForm):
	class Meta:
		model = Manager
		fields = ['name', 'gender', 'tel', 'home_addr', 'acct_bank', 'acct_name', 
			'acct_no', 'kin_name', 'kin_tel', 'kin_relationship'
		]
