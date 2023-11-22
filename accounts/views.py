from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Contact
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

# login function
def login_view(request):
	# collect info from form

	if request.user.is_authenticated:
		return redirect("store:product_list")
	if request.method == "POST":
		email = request.POST.get("email")
		password = request.POST.get("password")

		# collect user from database and check if exists
		user = authenticate(request, username=email, password=password)
		print(user)
		if user is not None:
			login(request, user)
			# send an email to the user notifying his login
			return redirect("store:product_list")

		# The user input incorrect login credentials
		# return a message using message context processor
		messages.info(request, "The email or password incorrect")
		# redirect the user to the login page
		return redirect("account:login")

	# if the request method is get
	template = "accounts/auth/login.html"
	context = None
	return render(request, template, context)


# logout view
def logout_view(request):
	logout(request)
	# redirect the user to the login page
	return redirect("account:login")


# create an account for the user
def create_account(request):

	if request.method == "POST":
		# collect credentials from form
		email = request.POST.get("email")
		password = request.POST.get("password1")
		conf_password = request.POST.get("password2")

		if password == conf_password:
			try :
				# check if the user does exists, through emails
				email_exists = CustomUser.objects.get(email = email)
				# dispaly the message
				messages.info(request, "The email exists")
				return redirect("account:register")
				# the email does not exists
			except ObjectDoesNotExist:
				# create an account for user
				user = CustomUser(
					email = email,
					)
				user.set_password(password)
				user.save()
				messages.success(request, "You have successfully created an account")
				# send an email to validate the email

				# Prepare email content
				subject = 'Confirm email'
				recipient_list = [user.email,]

				# Create an EmailMultiAlternatives instance
				email_instance = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, recipient_list)

				# Plain text content
				text_message = ''
				email_instance.body = text_message

				url = request.build_absolute_uri(reverse(
					"account:confirm_email", args = [user.email]
					))

				# HTML content
				html_message = render_to_string('accounts/emails/conf_email.html', {'email': user.email,
					'url' : url,
					})
				email_instance.attach_alternative(html_message, 'text/html')

				# Attach files (optional)
				# email.attach_file('/path/to/file.txt')

				# Send the email
				email_instance.send()

				# login the user
				user = authenticate(request, username=email, password=password)
				if user is not None:
					login(request, user)
					return redirect("store:product_list")
				messages.error(request, "Something went wrong, please log in.")
				return redirect("account:login")
		else:
			messages.error(request, "Password does not match!")
			return redirect("account:register")

	# if the request method is get
	# template path
	template = "accounts/auth/create_account.html"
	context = None


	return render (request, template, context)

# confirm email
def confirm_email(request, email):
	
	user = get_object_or_404(CustomUser, email=email, confirm_email = False)

	user.confirm_email = True
	user.save()

	messages.info(request, "Thank you for confirming your email address.")

	return redirect("account:login")



# forgot password method
def forgot_password(request):
	
	if request.method == "POST":
		# collect email and send email to the user
		email_address = request.POST.get('email')


		# Prepare email content
		subject = 'Forgot Password'
		recipient_list = [email_address,]

		# Create an EmailMultiAlternatives instance
		email = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, recipient_list)

		# Plain text content
		text_message = ''
		email.body = text_message

		# build a link to redirect a user to change password
		url = request.build_absolute_uri(reverse("account:forgot_password_change", args = (email_address,)))

		# HTML content
		html_message = render_to_string('accounts/emails/forgot_password.html', {'email': email_address,
			'url' : url,
			})
		email.attach_alternative(html_message, 'text/html')

		# Attach files (optional)
		# email.attach_file('/path/to/file.txt')

		# Send the email
		email.send()

		# render message
		messages.success(request, "Please check your mail box.")
		return redirect("account:login")


	template = "accounts/auth/email_form.html"
	context = None
	return render(request, template, context)


# change password for the forgot password user

def forgot_password_change(request, email):

	if request.method == "POST":
		
		password = request.POST.get('password1')
		conf_password = request.POST.get('password2')

		if password == conf_password :

			try :
				# get the user
				user = CustomUser.objects.get(email = email)
				# change password
				user.set_password(password)
				user.save()
				messages.success(request, "You have successfully changed your password")
				# Prepare email content
				subject = 'Password Changed'
				recipient_list = [email,]

				# Create an EmailMultiAlternatives instance
				email_instance = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, recipient_list)

				# Plain text content
				text_message = ''
				email_instance.body = text_message

				# HTML content
				html_message = render_to_string('accounts/emails/change_password.html', {'email': email})
				email_instance.attach_alternative(html_message, 'text/html')


				# Send the email
				email_instance.send()

				return redirect("account:login")

			except ObjectDoesNotExist:

				messages.error(request, "The account does not exists, please create an account.")
				return redirect("account:register")
		else:
			messages.error(request, "Password does not match.")
			return redirect("account:forgot_password_change")

	template = "accounts/auth/forgot_password.html"
	context = {'url' : request.build_absolute_uri(reverse(
		"account:forgot_password_change", args = [email,]
		))
	}
	return render(request, template, context)



# contact view
def contact(request):

	if request.method == "POST":
		name = request.POST.get("name")
		email = request.POST.get("email")
		message = request.POST.get("message")

		contact = Contact(
			name = name,
			email = email,
			message = message
			)
		contact.save()
		messages.success(request, "You have successfully sent contact.")
		return redirect("account:contact")

	template = "store/main/contact.html"
	context = None 
	return render(request, template, context)

