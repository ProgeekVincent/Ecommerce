from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User model fields
# Custom user model inherit from the AbstractUser class
class CustomUser(AbstractUser):

	confirm_email = models.BooleanField(default=False, verbose_name="email confirmed")

	def __str__(self):
		return f'{self.username}\n{self.first_name}, {self.last_name}'


class Contact(models.Model):

	name = models.CharField(max_length=100)
	email = models.EmailField()
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name