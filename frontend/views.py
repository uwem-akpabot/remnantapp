from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from userprofile.models import Userprofile
from customer.models import Customer, Teller, Manager
from account.models import Company_account
#from contribution.models import Contribution

COMPANY = 'Remnant Multipurpose Daily/Monthly Savings'

def index(request):
	customers = Customer.objects.all()
	return render(request, 'frontend/homepage.html', {'customers': customers, 'company': COMPANY})

def dashboard(request):
	customers = Customer.objects.all()
	count_customers = Customer.objects.all()

	count_tellers = Teller.objects.all() 
	count_managers = Manager.objects.all()
	count_users = count_customers.count() + count_tellers.count() + count_managers.count()

	company_account = Company_account.objects.latest('id')
	print(company_account)

	return render(request, 'frontend/dashboard.html', {'customers': customers, 'count_customers': count_customers, 
		'count_users': count_users, 'company_account': company_account, 'company': COMPANY})
	#return redirect('login')

@login_required
def create_account(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			user = form.save()
			account_type = request.POST.get('account_type', 'customer')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			name = f"{first_name} {last_name}"
			created_by = request.POST.get('created_by')

			if account_type == 'mgr':
				userprofile = Userprofile.objects.create(user=user, is_mgr=True, first_name=first_name, last_name=last_name, created_by=created_by)
				managerprofile = Manager.objects.create(user=user, name=name, created_by=created_by)
				userprofile.save()
				managerprofile.save()
			elif account_type == 'teller':
				userprofile = Userprofile.objects.create(user=user, is_teller=True, first_name=first_name, last_name=last_name, created_by=created_by)
				tellerprofile = Teller.objects.create(user=user, name=name, created_by=created_by)
				userprofile.save()
				tellerprofile.save()
			else:
				userprofile = Userprofile.objects.create(user=user, is_cust=True, first_name=first_name, last_name=last_name, created_by=created_by)
				customerprofile = Customer.objects.create(user=user, name=name, created_by=created_by)
				userprofile.save()
				customerprofile.save()

			msg_title = 'New Record!'
			msg_text = 'User has been created successfully!'
			messages.add_message(request, messages.SUCCESS, msg_text, extra_tags=msg_title)

			#login(request, user)
			#return redirect('index')
			return redirect('create_account')

		else:
			msg_title = 'Error!'
			msg_text = 'Record was NOT saved!'
			messages.add_message(request, messages.ERROR, msg_text, extra_tags=msg_title)

	else:
		form = UserCreationForm()
	return render(request, 'frontend/create_account.html', {'form': form, 'company': COMPANY})
