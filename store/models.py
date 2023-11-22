from django.db import models
from django.urls import reverse



# Other images model 
class Image(models.Model):
	image = models.ImageField(upload_to="images/products/others/")

	def __str__(self):
		return f"{self.image}"

# category model
class Category(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to="images/products/categories/", blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name


# subcategory model
class SubCategory(models.Model):
	name = models.CharField(max_length=100)
	category = models.ForeignKey(Category, related_name="category_items", on_delete=models.CASCADE,)
	description = models.TextField()

	def __str__(self):
		return self.name

# products model

class Product(models.Model):


	name = models.CharField(max_length=300)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = "product_category")
	slug = models.SlugField(max_length=10000, unique=True)
	image = models.ImageField(upload_to="images/products/main/", verbose_name="main image")
	other_image = models.ManyToManyField(Image, verbose_name="other images")
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField()
	published = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	available = models.BooleanField(default=True)



	def __str__(self):
		return f"{self.name}"



	def get_absolute_url(self):
		return reverse("store:product_detail", args=[self.id,
													self.slug]
						)


	class Meta:
		ordering = ['published', 'updated']