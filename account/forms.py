from django import forms
from contribution.models import Account

class AddAccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['contribution_month', 'contribution_year', 'date_charged']