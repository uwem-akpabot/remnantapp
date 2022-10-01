from django.contrib.auth.models import User
from django.db import models

class Userprofile(models.Model):
	user = models.OneToOneField(User, related_name='Userprofile', on_delete=models.CASCADE)
	is_dir = models.BooleanField(default=False)
	is_mgr = models.BooleanField(default=False)
	is_teller = models.BooleanField(default=False)
	is_cust = models.BooleanField(default=False)
	first_name = models.CharField(max_length=35, blank=True, null=True)
	last_name = models.CharField(max_length=35, blank=True, null=True)
	created_by = models.CharField(max_length=100, blank=True, null=True)

User.userprofile = property(lambda u:Userprofile.objects.get_or_create(user=u)[0])
