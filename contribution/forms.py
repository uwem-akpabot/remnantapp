from django import forms
from .models import Contribution, Withdrawal

class AddContributionForm(forms.ModelForm):
	class Meta:
		model = Contribution
		fields = ['customer', 'contribution_day', 'contribution_month', 
			'contribution_year', 'amount_paid', 'transaction', 
			'payment_plan', 'recorded_by']

class WithdrawalForm(forms.ModelForm):
	class Meta:
		model = Withdrawal
		fields = ['customer', 'amount', 'withdrawal_date', 'recorded_by']