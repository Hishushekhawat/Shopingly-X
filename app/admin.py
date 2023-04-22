from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Customer)
class CusomerModelAdmin(admin.ModelAdmin):
	list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display = ['id','title','selling_prize','discount_prize','description','brand','category','product_image']

@admin.register(Orderplaced)
class OrderplacedModelAdmin(admin.ModelAdmin):
	list_display = ['id','user','customer','product','quantity','ordered_date','status']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
	list_display = ['id','user','product','quantity']