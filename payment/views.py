from django.shortcuts import render, redirect, get_object_or_404
import braintree
from django.conf import settings
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
@login_required(login_url="account:login")
def payment_process(request):

	order_id = request.session.get('order_id')
	order = get_object_or_404(Order, id=order_id)
	total_cost = order.get_total_cost()

	if request.method == "POST":

		nonce = request.POST.get('payment_method_nonce', None)

		result = gateway.transaction.sale(
			{
				'amount' : f'{total_cost:2f}',
				'payment_method_nonce' : nonce,
				'options' : {
						'submit_for_settlement' : True
				}
			})

		if result.is_success :

			order.paid = True
			order.braintree_id = result.transaction.id
			order.save()

			# Prepare email content
			subject = 'Payment successful.'
			recipient_list = [order.email,]

			# Create an EmailMultiAlternatives instance
			email_instance = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, recipient_list)

			# Plain text content
			text_message = ''
			email_instance.body = text_message

			# HTML content
			html_message = render_to_string('store/payments/email.html', 
				{
					'order': order,
					'products' : order.items.all()
				 })
			email_instance.attach_alternative(html_message, 'text/html')

			# Attach files (optional)
			# email.attach_file('/path/to/file.txt')

			# Send the email
			email_instance.send()

			return redirect('payments:payment_done')

		else:
			return redirect('payments:payment_canceled')
	else:

		client_token = gateway.client_token.generate()
		template = "store/payments/process.html"
		context = {
			'client_token' : client_token
		}
		return render(request, template, context)


def payment_done(request):

	template = 'store/payments/done.html'
	context = None
	return render(request, template, context)

def payment_canceled(request):

	template = 'store/payments/canceled.html'
	context = None
	return render(request, template, context)