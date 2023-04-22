from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
STATE_CHOICE = (
	('Anaman And Nicober Island','Anaman And Nicober Island'),
	('Andra Pradesh','Andra Pradesh'),
	('Arunchal Pradesh','Arunchal Pradesh'),
	('Assam','Assam'),
	('Bihar','Bihar'),
	('Chandigarh','Chandigarh'),
	('Chattisgarh','Chattisgarh'),
	('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
	('Daman and Diu','Daman and Diu'),
	('Delhi','Delhi'),
	('Goa','Goa'),
	('Gujarat','Gujarat'),
	('Haryana','Haryana'),
	('Himachal Pradesh','Himachal Pradesh'),
	('Jammu & Kashmir','Jammu & Kashmir'),
	('Jharkhand','Jharkhand'),
	('Karnataka','Karnataka'),
	('Kerla','Kerla'),
	('Lakshadweep','Lakshadweep'),
	('Madhya Pradesh','Madhya Pradesh'),
	('Maharashtra','Maharashtra'),
	('Manipur','Manipur'),
	('Meghayala','Meghayala'),
	('Mizoram','Mizoram'),
	('Nagaland','Nagaland'),
	('Odissa','Odissa'),
	('Punjab','Punjab'),
	('Rajasthan','Rajasthan'),
	('Sikkim','Sikkim'),
	('Tamil Nadu','Tamil Nadu'),
	('Telangana','Telangana'),
	('Tripura','Tripura'),
	('Uttar Pradesh','Uttar Pradesh'),
	('Uttarakhand','Uttarakhand'),
	('West Bengal','West Bengal'),
	)

class Customer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	locality = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	zipcode = models.IntegerField()
	state = models.CharField(choices=STATE_CHOICE, max_length=100)

	def __str__(self):
		return str(self.id)

CATEGORY_CHOICE = (
	('M','Mobile'),
	('L','Laptop'),
	('TW','Top Wear'),
	('BW','Bottom Wear'),
	)

class Product(models.Model):
	title = models.CharField(max_length=100)
	selling_prize = models.FloatField(max_length=100)
	discount_prize = models.FloatField(max_length=100)
	description = models.TextField(max_length=100)
	brand = models.CharField(max_length=100)
	category = models.CharField(choices=CATEGORY_CHOICE, max_length=2)
	product_image = models.ImageField(upload_to='productimg/')

	def __str__(self):
		return str(self.id)

	# def save(self):
	# 	super().save()

	# 	img = Image.open(self.image.path)

	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)


STATUS_CHOICE = (
	('Accepted','Accepted'),
	('Packed','Packed'),
	('On_the_way','On_the_way'),
	('Delivered','Delivered'),
	('Canceled','Canceled'),
	)

class Orderplaced(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE) 
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	ordered_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(choices=STATUS_CHOICE, max_length=20, default='Pending')

	def __str__(self):
		return str(self.id)

	@property
	def total_prize(self):
		return self.quantity*self.product.discount_prize


class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	@property
	def total_cost(self):
		return self.quantity*self.product.discount_prize