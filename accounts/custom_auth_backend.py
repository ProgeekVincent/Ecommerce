from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import CustomUser

class EmailBackend(ModelBackend):
	# overriding the authenticate method to use the email as the log in credential
	def authenticate(self, request, username=None, password=None, **kwargs):
		# get the current active user model "CustomUser"
		user_model = get_user_model()
		try :
			# get the user by email, from the username field
			user = user_model.objects.get(email=username)
		except user_model.DoesNotExist:
			# The user email does not exist
			return None

		# check the password correspondence
		if user.check_password(password):
			return user


		def get_user (self, user_id):
			user_model = get_user_model()

			try :
				return user_model.objects.get(pk=user_id)
			except user_model.DoesNotExist:
				return None
