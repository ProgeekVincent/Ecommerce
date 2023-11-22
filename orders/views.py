from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

@login_required(login_url="account:login")
def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order,
					product=item['product'],
					price=item['price'],
					quantity=item['quantity'])

			request.session['order_id'] = order.id
			# clear the cart
			cart.clear()
		# redirect the user to the braintree gateway server page
		return redirect("payments:payment_process")
	else:
		form = OrderCreateForm()
		template = "store/orders/create.html"
		context = {
			"cart" : cart,
			"form" : form
		}
		return render(request, template, context)