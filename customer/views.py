from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, Teller, Manager
from contribution.models import Contribution, Cust_contrb
from account.models import Company_account, Contribution_account
from .forms import AddCustomerForm, AddTellerForm, AddManagerForm
from contribution.forms import AddContributionForm
from django.contrib import messages

company = 'Remnant Multipurpose'

#Browse all
@login_required
def customer(request):
	customers = Customer.objects.all()
	return render(request,'customer/customer.html', {'company':company, 'customers': customers})

@login_required
def teller(request):
	tellers = Teller.objects.all()
	return render(request,'teller/teller.html', {'company':company, 'tellers': tellers})

@login_required
def manager(request):
	managers = Manager.objects.all()
	return render(request,'manager/manager.html', {'company':company, 'managers': managers})


#Get detail by Id
@login_required
def customer_detail(request, customer_id):
	customer = Customer.objects.get(pk=customer_id)
	return render(request, 'customer/customer_detail.html', {'company':company, 'customer': customer})

@login_required
def teller_detail(request, teller_id):
	teller = Teller.objects.get(pk=teller_id)
	return render(request, 'teller/teller_detail.html', {'company':company, 'teller': teller})

@login_required
def manager_detail(request, manager_id):
	manager = Manager.objects.get(pk=manager_id)
	return render(request, 'manager/manager_detail.html', {'company':company, 'manager': manager})


#Update user record
@login_required
def update_customer(request, customer_id):
	customer = Customer.objects.get(pk=customer_id)
	form = AddCustomerForm(instance=customer)

	if request.method == 'POST':
		form = AddCustomerForm(request.POST, instance=customer) #if submit is click and form method is POST

		if form.is_valid():
			customer = form.save() #save to database

			msg_title = 'Updated!'
			msg_text = 'Customer is saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('customer')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = AddCustomerForm() #if submit is not clicked, display empty form

	return render(request, 'customer/update_customer.html', {'form': form, 'company':company, 'customer': customer})


@login_required
def update_teller(request, teller_id):
	teller = Teller.objects.get(pk=teller_id)
	form = AddTellerForm(instance=teller)

	if request.method == 'POST':
		form = AddTellerForm(request.POST, instance=teller) #if submit is click and form method is POST

		if form.is_valid():
			teller = form.save() #save to database

			msg_title = 'Updated!'
			msg_text = 'Teller is saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('teller')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = AddTellerForm() #if submit is not clicked, display empty form

	return render(request, 'teller/update_teller.html', {'form': form, 'company':company, 'teller': teller})


@login_required
def update_manager(request, manager_id):
	manager = Manager.objects.get(pk=manager_id)
	form = AddManagerForm(instance=manager)

	if request.method == 'POST':
		form = AddManagerForm(request.POST, instance=manager) #if submit is click and form method is POST

		if form.is_valid():
			manager = form.save() #save to database

			msg_title = 'Updated!'
			msg_text = 'Manager is saved successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)
			return redirect('manager')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = AddManagerForm() #if submit is not clicked, display empty form

	return render(request, 'manager/update_manager.html', {'form': form, 'company':company, 'manager': manager})


#Delete user record
@login_required
def delete_customer(request, customer_id):
	customer = Customer.objects.get(pk=customer_id)

	if request.method == 'POST':
		customer.delete()

		msg_title = 'Deleted!'
		msg_text = 'Customer was deleted successfully!'
		messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)

		return redirect('customer')

	return render(request, 'customer/delete_customer.html', {'company':company, 'customer': customer})

@login_required
def delete_teller(request, teller_id):
	teller = Teller.objects.get(pk=teller_id)

	if request.method == 'POST':
		teller.delete()

		msg_title = 'Deleted!'
		msg_text = 'Teller was deleted successfully!'
		messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)

		return redirect('teller')

	return render(request, 'teller/delete_teller.html', {'company':company, 'teller': teller})

@login_required
def delete_manager(request, manager_id):
	manager = Manager.objects.get(pk=manager_id)

	if request.method == 'POST':
		manager.delete()

		msg_title = 'Deleted!'
		msg_text = 'Manager was deleted successfully!'
		messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)

		return redirect('manager')

	return render(request, 'manager/delete_manager.html', {'company':company, 'manager': manager})

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




@login_required
def add_customer(request):
	if request.method == 'POST':
		form = AddCustomerForm(request.POST) #if submit is click and form method is POST

		if form.is_valid():
			customer = form.save() #save to database
			return redirect('add_customer') #take us back to index page
	else:
		form = AddCustomerForm() #if submit is not clicked, display empty form


	return render(request, 'customer/add_customer.html', {'company':company})
"""
