from django.urls import path
from . import views

urlpatterns = [
	path('', views.contribution_mgr, name= 'contribution_mgr'),
	path('contribution/<int:customer_id>/', views.customer_contribution, name='customer_contribution'),
	path('withdrawal/<int:customer_id>/', views.customer_withdrawal, name='customer_withdrawal'),
	path('contribution-record/', views.contribution_record, name='contribution_record'),

	path('add_contribution/', views.add_contribution, name= 'add_contribution'),
	path('<int:customer_id>/', views.contribution_detail, name='contribution_detail'),
	path('update/<int:customer_id>/', views.update_contribution, name='update_contribution'),
	path('delete/<int:customer_id>/', views.delete_contribution, name='delete_contribution'),
	path('contrb_percustomer/<int:customer_id>/', views.contribution_percustomer, name='contribution_percustomer'),
	path('all_custcontrb_balance/', views.all_custcontrb_balance, name='all_custcontrb_balance'),
]
