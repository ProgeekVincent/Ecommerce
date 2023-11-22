from django.urls import path
from .views import *


app_name = "account"
urlpatterns = [

	path('login/', login_view, name="login"),
	path('register/', create_account, name='register'),
	path('logout/', logout_view, name='logout'),
	path('forgot_password/', forgot_password, name="forgot_password"),
	path('forgot_password/change/<str:email>/', forgot_password_change, name="forgot_password_change"),
	path('confirm/email/<str:email>/', confirm_email, name="confirm_email"),
	path('contact/', contact, name="contact")

]
