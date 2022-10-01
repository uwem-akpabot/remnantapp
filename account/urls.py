from django.urls import path
from . import views

urlpatterns = [
	path('set-contribution-period/', views.set_current_contribution_period, name= 'set_current_contribution_period'),
	path('company-account/', views.company_acct, name='company_acct'),
	path('reports/', views.reports, name='reports'),
	path('user-account-summary/<int:customer_id>/', views.user_account_summary, name='user_account_summary'),
	path('user-transaction-details/<int:customer_id>/', views.user_transaction_details, name='user_transaction_details'),
	path('user-wallet-balance/<int:customer_id>/', views.user_wallet_balance, name='user_wallet_balance'),
	#path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
	#path('customer/update/<int:customer_id>/', views.update_customer, name='update_customer'),
]
