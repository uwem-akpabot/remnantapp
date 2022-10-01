from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='homepage'),
	path('auth/', views.dashboard, name='dashboard'),
	path('create_account/', views.create_account, name='create_account'),
]
