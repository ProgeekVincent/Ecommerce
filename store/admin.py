from django.contrib import admin
from .models import Product, Image, Category, SubCategory


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'description')


@admin.register(Category)
class Category(admin.ModelAdmin):
	list_display = ('name', 'description')



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('available', 'name', 'slug', 'price', 'description', 'image', 'published', 'updated')

	list_filter = ('available', 'price', 'description')

	prepopulated_fields = {
		'slug' : ('name', 'price', 'description')
	}
	ordering = ['-published',]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ('image',)