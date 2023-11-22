from django.urls import path
from .views import payment_done, payment_canceled, payment_process


app_name = "payments" 

urlpatterns = [
	path("process/", payment_process, name="payment_process"),
	path("done/", payment_done, name="payment_done"),
	path("canceled", payment_canceled, name="payment_canceled")
]