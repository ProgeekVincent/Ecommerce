from django.urls import path
from .views import *

app_name = 'store'

urlpatterns = [
	path('', home, name="home"),
	path('discover/<int:id>/', discover, name="discover"),
	path('product/list/', product_list, name="product_list"),
	path('product/detail/<int:id>/<slug:slug>/', product_detail, name="product_detail"),
	path('<int:id>/', sub_category_products, name="sub_category_products")
]