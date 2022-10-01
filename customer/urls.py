from django.urls import path
from . import views

urlpatterns = [
	#customer
	path('customer/', views.customer, name= 'customer'),
	path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
	path('customer/update/<int:customer_id>/', views.update_customer, name='update_customer'),
	path('customer/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
	#teller
	path('teller/', views.teller, name='teller'),
	path('teller/<int:teller_id>/', views.teller_detail, name='teller_detail'),
	path('teller/update/<int:teller_id>/', views.update_teller, name='update_teller'),
	path('teller/delete/<int:teller_id>/', views.delete_teller, name='delete_teller'),\
	#manager
	path('manager/', views.manager, name='manager'),
	path('manager/<int:manager_id>/', views.manager_detail, name='manager_detail'),
	path('manager/update/<int:manager_id>/', views.update_manager, name='update_manager'),
	path('manager/delete/<int:manager_id>/', views.delete_manager, name='delete_manager'),
]
