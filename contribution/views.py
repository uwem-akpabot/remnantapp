from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from customer.models import Customer
from .models import Contribution, Cust_contrb, Account, Withdrawal
from account.models import Company_account, Admin_total_funds
from .forms import AddContributionForm, WithdrawalForm
from django.contrib import messages

company = 'Remnant Multipurpose'

# Done, working, in use
@login_required
def contribution_mgr(request):
	customers = Customer.objects.all()
	return render(request,'contribution/contribution_mgr.html', {'company':company, 'customers': customers})

# Done, working, in use
#ADD CONTRIBUTION
@login_required
def customer_contribution(request, customer_id):
	customer = Customer.objects.get(pk=customer_id)
	customers = Customer.objects.all()

	#ACCORDION 2: Contribution history
	contrb_percustomer = Contribution.objects.filter(customer_id=customer_id)

	if request.method == 'POST':
		form = AddContributionForm(request.POST) #if submit is clicked and form method is POST
		#print(request.POST.get(customer_id))
		if form.is_valid():
			contribution = form.save() #1. Save filled form record to Contribution table
			cust = request.POST.get('customer') #Grab the selected customer id while filling AddContribution form
			payment_plan = request.POST.get('payment_plan') #Grab the selected payment_plan while filling AddContribution form
			contribution_period = f"{request.POST.get('contribution_month')} {request.POST.get('contribution_year')}"

			try:
				if not Cust_contrb.objects.filter(customer_id=cust).exists():
					cust_contrb = Cust_contrb.objects.create(customer_id=cust)
				else:
					cust_contrb = Cust_contrb.objects.get(customer_id=cust) #create a row for new customer with balance and customer_id column in Cust_contrb table

				#perform the calculatn logic
				specific_customer = Cust_contrb.objects.filter(customer_id=cust) #locate row of customer whose customer id is form selected custmer id in Cust_contrb table
				for iterated in specific_customer:
					bal = int(iterated.total) #get current balance for this row, b4 adding new amount
					days = int(iterated.duration) #get current duration for this row, b4 adding new amount
					chg = int(iterated.charges) #get current duration for this row, b4 adding new amount
					setcon_perd = iterated.set_current_contrib_period #get set_contribution_period for this row, b4 adding new amount
					deduct_com = iterated.deducted_commission_for #get deducted_commission_for for this row, b4 adding new amount

				cust_contrb.total = bal + int(request.POST.get('amount_paid')) #update the balance column in Cust_contrb table
				cust_contrb.charges = int(payment_plan)
				cust_contrb.contribution_period = contribution_period

				#FIRST DEPOSIT OF MONTH; USER IS CHARGED 
				
				# 1. Charged! New User's First Ever Deposit
				if days == 0:
					print('Charged! New User First Deposit')
					cust_contrb.deducted_commission_for = contribution_period #input this contribution_period in deducted_commission_for
					cust_contrb.set_current_contrib_period = contribution_period #Bcos column is blank for new user, fill in the chosen contrb period 
					cust_contrb.total = bal + int(request.POST.get('amount_paid')) #update the balance column in Cust_contrb table
					cust_contrb.wallet = cust_contrb.total - cust_contrb.charges #then, subtract the charge
					cust_contrb.duration = 1 #set to start from beginnning
					
					#SEND MONEY TO COMPANY ACCOUNT
					comp_acct = Company_account.objects.create(amount=0)
					comp_acct.transaction_type = 'Deposit'
					comp_acct.transaction_detail = f"{cust_contrb.customer.name}'s contribution - {contribution_period}"
					comp_acct.amount = cust_contrb.charges
					comp_acct.save()

					admin_total_funds = Admin_total_funds.objects.get(id=1)
					admin_total_funds.balance = cust_contrb.charges + int(admin_total_funds.balance) #add record to admin_total_funds table
					admin_total_funds.save()

				#OTHER DEPOSITS OF MONTH AFTER BEING CHARGED; USER IS NOT CHARGED AGAIN FOR THIS MONTH
				
				# 2. Charged! Existing User's First Deposit of the Month
				elif days > 0 and deduct_com != setcon_perd:
					print('Charged! Existing Users First Deposit of the Month')
					cust_contrb.deducted_commission_for = contribution_period #input this contribution_period in deducted_commission_for
					add_to_wallet = int(request.POST.get('amount_paid')) - cust_contrb.charges #perfrom calc
					print(f'Addtowallet: {add_to_wallet}')
					print(f'cust_contrb.wallet b4: {cust_contrb.wallet}')
					cust_contrb.wallet = int(cust_contrb.wallet) + int(add_to_wallet) #update wallet value
					print(f'cust_contrb.wallet aft: {cust_contrb.wallet}')

					cust_contrb.total = bal + int(request.POST.get('amount_paid')) #update the balance column in Cust_contrb table
					cust_contrb.duration = 1 
					
					#SEND MONEY TO COMPANY ACCOUNT
					comp_acct = Company_account.objects.create(amount=0)
					comp_acct.transaction_type = 'Deposit'
					comp_acct.transaction_detail = f"{cust_contrb.customer.name}'s contribution - {contribution_period}"
					comp_acct.amount = cust_contrb.charges
					comp_acct.save()

					admin_total_funds = Admin_total_funds.objects.get(id=1)
					admin_total_funds.balance = cust_contrb.charges + int(admin_total_funds.balance) #add record to admin_total_funds table
					admin_total_funds.save()

					#SEND MONEY TO BOTH CUSTOMER'S WALLET AND CONTRIBUTION ACCOUNT
					"""
					comp_acct = Company_account.objects.create(amount=0)
					comp_acct.amount = cust_contrb.charges #send the deducted charge to company
					comp_acct.transaction_type = 'Deposit'
					comp_acct.transaction_detail = f'Contribution for {contribution_period} from Customer ID: {cust_contrb.customer_id}'
					comp_acct.curr_balance += int(comp_acct.amount)
					"""						
				
				# 3. Not charged! Users Other Deposits of the Month
				elif days > 0 and contribution_period == setcon_perd:
					cust_contrb.wallet = int(cust_contrb.wallet) + int(request.POST.get('amount_paid'))
					cust_contrb.duration = days + int(1) #increase the day by one (payment duration)
					print('Not charged! Users Other Deposits of the Month')
					print(deduct_com)
					print(setcon_perd)
					print(days)

					#DO NOT SEND MONEY TO COMPANY ACCOUNT

				else:
					pass

				cust_contrb.save() #2. Also save record to Cust_contrb table

			except Cust_contrb.DoesNotExist:
				cust_contrb = None

			msg_title = 'New Record!'
			msg_text = 'Contribution is saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('contribution_mgr')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = AddContributionForm() #if submit is not clicked, display empty form

	return render(request, 'contribution/customer_contribution.html', {'company':company, 'customer': customer, 'customers': customers, 'contrb_percustomer': contrb_percustomer})

# Done, working, in use
@login_required
def contribution_record(request):
	customers = Customer.objects.all()
	cust_contrbs = Cust_contrb.objects.all()
	contrb_details = Contribution.objects.all()
	return render(request,'contribution/contribution_record.html', {'company':company, 'customers': customers, 'cust_contrbs': cust_contrbs, 'contrb_details':contrb_details})

#Doing, working on it
#WITHDRAWAL
@login_required
def customer_withdrawal(request, customer_id):
	customer = Customer.objects.get(pk=customer_id)
	cust_contrb = Cust_contrb.objects.get(customer_id=customer_id)

	#ACCORDION 2: Withdrawal history
	wthdw_percustomer = Withdrawal.objects.filter(customer_id=customer_id)

	if request.method == 'POST':
		form = WithdrawalForm(request.POST) #if submit is clicked and form method is POST
		#print(request.POST.get(customer_id))
		
		if form.is_valid():
			withdrawal = form.save() #1. Save filled form record to Contribution table
			# payment_plan = request.POST.get('payment_plan') #Grab the selected payment_plan while filling AddContribution form
			# contribution_period = f"{request.POST.get('contribution_month')} {request.POST.get('contribution_year')}"

			try:
				if not Withdrawal.objects.filter(customer_id=customer).exists():
					pass
					# customer does not exist
				else:
					specific_customer = Cust_contrb.objects.filter(customer_id=customer) #locate row of customer whose customer id is form selected custmer id in Cust_contrb table
					for iterated in specific_customer:
						wallet = int(iterated.wallet) #get current wallet for this row, b4 sbtractg new amount
						# cust_contrb.total = bal + int(request.POST.get('amount_paid')) #update the balance column in Cust_contrb table
				
					cust_contrb.amount = int(request.POST.get('amount')) #update the balance column in Cust_contrb table
					cust_contrb.wallet = wallet - cust_contrb.amount 
					
					#SUBTRACT MONEY FROM COMPANY ACCOUNT
					comp_acct = Company_account.objects.create(amount=0)
					comp_acct.transaction_type = 'Withdrawal'
					comp_acct.transaction_detail = f"{cust_contrb.customer.name}'s withdrawal from wallet"
					comp_acct.amount = cust_contrb.amount
					# comp_acct.curr_balance = int(comp_acct.curr_balance) + cust_contrb.charges #send the deducted charge to company
					comp_acct.save()

					admin_total_funds = Admin_total_funds.objects.get(id=1)
					admin_total_funds.balance = int(admin_total_funds.balance) - cust_contrb.amount #sbtract record from admin_total_funds table
					admin_total_funds.save()

				# # 2. Charged! Existing User's First Deposit of the Month
				# elif days > 0 and deduct_com != setcon_perd:
				# 	print('Charged! Existing Users First Deposit of the Month')
				# 	cust_contrb.deducted_commission_for = contribution_period #input this contribution_period in deducted_commission_for
				# 	add_to_wallet = int(request.POST.get('amount_paid')) - cust_contrb.charges #perfrom calc
				# 	print(f'Addtowallet: {add_to_wallet}')
				# 	print(f'cust_contrb.wallet b4: {cust_contrb.wallet}')
				# 	cust_contrb.wallet = int(cust_contrb.wallet) + int(add_to_wallet) #update wallet value
				# 	print(f'cust_contrb.wallet aft: {cust_contrb.wallet}')

				# 	cust_contrb.total = bal + int(request.POST.get('amount_paid')) #update the balance column in Cust_contrb table
				# 	cust_contrb.duration = 1 
					
				# 	#SEND MONEY TO COMPANY ACCOUNT
				# 	comp_acct = Company_account.objects.create(amount=0)
				# 	comp_acct.transaction_type = 'Deposit'
				# 	comp_acct.transaction_detail = f"{cust_contrb.customer.name}'s contribution - {contribution_period}"
				# 	comp_acct.amount = cust_contrb.charges
				# 	#comp_acct.curr_balance = int(comp_acct.curr_balance) + cust_contrb.charges #send the deducted charge to company
				# 	comp_acct.save()

				# 	admin_total_funds = Admin_total_funds.objects.get(id=1)
				# 	admin_total_funds.balance = cust_contrb.charges + int(admin_total_funds.balance) #add record to admin_total_funds table
				# 	admin_total_funds.save()

				# 3. Not charged! Users Other Deposits of the Month
				# elif days > 0 and contribution_period == setcon_perd:
				# 	cust_contrb.wallet = int(cust_contrb.wallet) + int(request.POST.get('amount_paid'))
				# 	cust_contrb.duration = days + int(1) #increase the day by one (payment duration)
				# 	print('Not charged! Users Other Deposits of the Month')
				# 	print(deduct_com)
				# 	print(setcon_perd)
				# 	print(days)

					#DO NOT SEND MONEY TO COMPANY ACCOUNT

				cust_contrb.save() #2. Also save record to Cust_contrb table
				# comp_acct.save() #3. Also save record to comp_acct table

			except Cust_contrb.DoesNotExist:
				cust_contrb = None

			msg_title = 'New Record!'
			msg_text = 'Withdrawal is saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('contribution_mgr')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)
		
	else:
		form = WithdrawalForm() #if submit is not clicked, display empty form

	return render(request, 'contribution/withdrawal.html', {'company':company, 'customer': customer, 'cust_contrb': cust_contrb})


@login_required
def contribution_percustomer(request, customer_id):
	contrb_percustomer = Contribution.objects.filter(customer_id=customer_id)
	customer = Customer.objects.get(pk=customer_id)
	return render(request,'contribution/contrb_percustomer.html', {'company':company, 'contrb_percustomer': contrb_percustomer, 'customer': customer})


@login_required
def contribution(request):
	contributions = Contribution.objects.all()
	customers = Customer.objects.all()
	return render(request,'contribution/contribution.html', {'company':company, 'contributions': contributions, 'customers': customers})

@login_required
def all_custcontrb_balance(request):
	custcontrb = Cust_contrb.objects.all()
	return render(request,'contribution/all_custcontrb.html', {'company':company, 'custcontrb': custcontrb})

@login_required
def add_contribution(request):
	customer = Customer.objects.all()

	if request.method == 'POST':
		form = AddContributionForm(request.POST) #if submit is click and form method is POST
		#print(request.POST.get(customer_id))
		if form.is_valid():
			contribution = form.save() #1. Save filled form record to Contribution table
			cust = request.POST.get('customer') #Grab the selected customer id while filling AddContribution form
			transaction = request.POST.get('transaction') #Grab the selected descriptn while filling AddContribution form

			try:
				if not Cust_contrb.objects.filter(customer_id=cust).exists():
					cust_contrb = Cust_contrb.objects.create(customer_id=cust)
				else:
					cust_contrb = Cust_contrb.objects.get(customer_id=cust) #create a row for new customer with balance and customer_id column in Cust_contrb table

				#perform the calculatn logic
				curr_amt = Cust_contrb.objects.filter(customer_id=cust) #locate row of customer whose customer id is form selected custmer id in Cust_contrb table
				for cc in curr_amt:
					c = int(cc.total) #get current balance for this row, b4 adding new amount

				#check user's choice, if to add or subtract frm current balance
				if transaction == 'Deposit':
					cust_contrb.total = c + int(request.POST.get('amount')) #update the balance column in Cust_contrb table
				elif transaction == 'Withdrawal': #withdrawal
					cust_contrb.total = c - int(request.POST.get('amount')) #update the balance column in Cust_contrb table
				else:
					pass

				cust_contrb.save() #2. Also save record to Cust_contrb table

			except Cust_contrb.DoesNotExist:
				cust_contrb = None

			"""
			try:
				cust_contrb = Cust_contrb.objects.get(customer_id=cust) #create a row for new customer with balance and customer_id column in Cust_contrb table

				#perform the calculatn logic
				curr_amt = Cust_contrb.objects.filter(customer_id=cust) #locate row of customer whose customer id is form selected custmer id in Cust_contrb table
				for cc in curr_amt:
					c = int(cc.balance) #get current balance for this row, b4 adding new amount

				#check user's choice, if to add or subtract frm current balance
				if description == 'Deposit':
					cust_contrb.balance = c + int(request.POST.get('amount')) #update the balance column in Cust_contrb table
				elif description == 'Withdrawal': #withdrawal
					cust_contrb.balance = c - int(request.POST.get('amount')) #update the balance column in Cust_contrb table
				else:
					pass

				cust_contrb.save() #2. Also save record to Cust_contrb table

			except Cust_contrb.DoesNotExist:
				cust_contrb = None
			"""

			msg_title = 'New Record!'
			msg_text = 'Contribution is saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('contribution')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = AddContributionForm() #if submit is not clicked, display empty form

	return render(request, 'contribution/add_contribution.html', {'form': form, 'company':company, 'customer':customer})


@login_required
def update_contribution(request, contribution_id):
	customer = Customer.objects.get()
	contribution = Contribution.objects.get(pk=contribution_id)

	form = AddContributionForm(instance=contribution)

	if request.method == 'POST':
		form = AddContributionForm(request.POST, instance=contribution) #if submit is click and form method is POST

		if form.is_valid():
			contribution = form.save() #save to database

			"""
			#update balance of contribution in cust_contrb table
			cust_contrbprofile = Cust_contrb.objects.create(customer=customer)
			"""

			msg_title = 'Updated!'
			msg_text = 'Contribution is saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('contribution')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = AddContributionForm() #if submit is not clicked, display empty form

	return render(request, 'contribution/update_contribution.html', {'form': form, 'company':company, 'customer':customer, 'contribution': contribution})


@login_required
def contribution_detail(request, customer_id):
	customer = Customer.objects.get(pk=customer_id)
	return render(request, 'customer/customer_detail.html', {'company':company, 'customer': customer})


@login_required
def delete_contribution(request, customer_id):
	customer = Customer.objects.get(pk=customer_id)

	if request.method == 'POST':
		customer.delete()

		msg_title = 'Deleted!'
		msg_text = 'Customer was deleted successfully!'
		messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)

		return redirect('customer')

	return render(request, 'customer/delete_customer.html', {'company':company, 'customer': customer})

"""
@login_required
def create_account(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			user = form.save()
			account_type = request.POST.get('account_type', 'customer')
			created_by = request.POST.get('created_by')

			if account_type == 'mgr':
				userprofile = Userprofile.objects.create(user=user, is_mgr=True, created_by=created_by)
				userprofile.save()
			elif account_type == 'teller':
				userprofile = Userprofile.objects.create(user=user, is_teller=True, created_by=created_by)
				userprofile.save()
			else:
				userprofile = Userprofile.objects.create(user=user, is_cust=True, created_by=created_by)
				customerprofile = Customer.objects.create(user=user, created_by=created_by)
				userprofile.save()
				customerprofile.save()

			#login(request, user)
			#return redirect('index')
			return redirect('create_account')
	else:
		form = UserCreationForm()
	return render(request, 'frontend/create_account.html', {'form': form, 'company': COMPANY})
"""
