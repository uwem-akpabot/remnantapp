from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contribution.models import Account, Cust_contrb, Contribution, Withdrawal
from .models import Company_account, Contribution_account, Admin_total_funds
from .forms import AddAccountForm
from django.contrib import messages

company = 'Remnant Multipurpose'

# Done, working, in use
@login_required
def set_current_contribution_period(request):
	#ACCORDION: past_contribution_periods_set
	past_contrb_periods = Account.objects.all()

	if request.method == 'POST':
		form = AddAccountForm(request.POST) #if submit is click and form method is POST

		if form.is_valid():
			account = form.save() #1. Save filled form record to Contribution table
			contrib_period = f"{request.POST.get('contribution_month')} {request.POST.get('contribution_year')}"
			cust_contrb = Cust_contrb.objects.filter().update(set_current_contrib_period=contrib_period)

			msg_title = 'New Record!'
			msg_text = 'Contribution period saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('customer')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = AddAccountForm() #if submit is not clicked, display empty form

	return render(request, 'account/set_contribution_period.html', {'form': form, 'company':company, 'past_contrb_periods': past_contrb_periods})


@login_required
def company_acct(request):
	#ACCORDION: company acct
	comp_accts = Company_account.objects.all()

	#ACCORDION: customers contribution acct
	cust_contrib_accts = Contribution_account.objects.all()

	return render(request, 'account/company_acct.html', {'company':company, 'comp_accts': comp_accts, 'cust_contrib_accts': cust_contrib_accts})


@login_required
def reports(request):
	admin_total_funds = Admin_total_funds.objects.all()
	cust_contrb = Cust_contrb.objects.all()
	company_acct = Company_account.objects.all()
	
	#ACCORDION: company acct
	comp_accts = Company_account.objects.all()

	#ACCORDION: customers contribution acct
	cust_contrib_accts = Contribution_account.objects.all()

	return render(request, 'account/reports.html', {'admin_total_funds': admin_total_funds, 'cust_contrb': cust_contrb, 
		'company_acct': company_acct, 'company':company})

@login_required
def user_account_summary(request, customer_id):
	cust_contrb = Cust_contrb.objects.get(customer_id=customer_id) #account summary
	# company_acct = Company_account.objects.get(customer_id=customer_id) #transaction details
	# admin_total_funds = Admin_total_funds.objects.get(customer_id=customer_id) #wallet balance

	return render(request, 'account/user_account_summary.html', {'cust_contrb': cust_contrb, 'company':company})

@login_required
def user_transaction_details(request, customer_id):
	contrb = Contribution.objects.filter(customer_id=customer_id) 
	withdraw = Withdrawal.objects.filter(customer_id=customer_id)
	# company_acct = Company_account.objects.get(customer_id=customer_id) #transaction details
	# admin_total_funds = Admin_total_funds.objects.get(customer_id=customer_id) #wallet balance

	return render(request, 'account/user_transaction_details.html', {'contrb': contrb, 'withdraw': withdraw, 'company':company})

@login_required
def user_wallet_balance(request, customer_id):
	cust_contrb = Cust_contrb.objects.get(customer_id=customer_id) #account summary
	# company_acct = Company_account.objects.get(customer_id=customer_id) #transaction details
	# admin_total_funds = Admin_total_funds.objects.get(customer_id=customer_id) #wallet balance

	return render(request, 'account/user_wallet_balance.html', {'cust_contrb': cust_contrb, 'company':company})

"""
@login_required
def contribution_period_history(request):
	history = Account.objects.all()
	return render(request,'account/account.html', {'company':company, 'history': history})

@login_required
def contribution_percustomer(request, customer_id):
	contrb_percustomer = Contribution.objects.filter(customer_id=customer_id)
	customer = Customer.objects.get(pk=customer_id)
	return render(request,'contribution/contrb_percustomer.html', {'company':company, 'contrb_percustomer': contrb_percustomer, 'customer': customer})

@login_required
def all_custcontrb_balance(request):
	custcontrb = Cust_contrb.objects.all()
	return render(request,'contribution/all_custcontrb.html', {'company':company, 'custcontrb': custcontrb})
"""
