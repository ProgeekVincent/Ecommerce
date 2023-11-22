from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, SubCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cart.forms import CartAddProductForm
from django.views.decorators.http import require_POST


def home(request):

	object_list = Category.objects.all()
	paginator = Paginator(object_list, 3)
	page_number = request.GET.get('page')

	try:
		categories = paginator.get_page(page_number)
	except PageNotAnInteger:
		categories = paginator.get_page(1)
	except EmptyPage:
		categories = paginator.get_page(paginator.num_pages)

	template = "store/main/index.html"
	context = {
		'categories' : categories,
		'page' : page_number
	}
	return render(request, template, context)

# discover products by category
def discover(request, id):
	
	category = get_object_or_404(Category, id=id)

	products = category.product_category.all()
	template = "store/main/discover.html"
	context = {
		'category' : category,
		'products' : products,
	}

	return render(request, template, context)

# query sub category items
def sub_category_products(request, id):

	sub_category = get_object_or_404(SubCategory, id=id)
	products = sub_category.category.product_category.all()

	templates = "store/main/sub_items.html"
	context = {
		"products" : products,
		"category" : sub_category.category
	}
	return render(request, templates, context)


# the product list page view

def product_list(request):

	object_list = Product.objects.filter(available=True)
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')

	try :
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	template = "store/main/product_list.html"
	context = {"products" : products, "page" : page }
	return render(request, template, context)


def product_detail(request, id, slug):

	product = get_object_or_404(Product, id=id, slug=slug)

	template = "store/main/product_detail.html"
	context = {"product" : product, 'form' : CartAddProductForm()}
	return render(request, template, context)