from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import UserRegistrationForm, CustomerProfileForm , ProductCreateForm, OrderUpdateForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decoraters import admin_only
from django.contrib.admin.views.decorators import staff_member_required


class ProductView(View):
	def get(self,request):
		topwears = Product.objects.filter(category='TW')
		bottomwears = Product.objects.filter(category='BW')
		mobiles = Product.objects.filter(category='M')
		laptops = Product.objects.filter(category='L')
		context = {
		 'topwears':topwears,
		 'bottomwears':bottomwears,
		 'mobiles':mobiles,
		 'laptops':laptops,
		}
		return render(request,'app/home.html',context)

class ProductDetailView(View):
	def get(self,request,pk):
		product = Product.objects.get(id=pk)
		item_already_exist = False
		if request.user.is_authenticated:
			item_already_exist = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		context = {
		 'product':product,
		 'item_already_exist':item_already_exist,
		}
		return render(request, 'app/productdetail.html',context)

@login_required
def add_to_cart(request):
	user = request.user
	product_id = request.GET.get('prod_id')
	product = Product.objects.get(id=product_id)
	Cart(user=user,product=product).save()
	return redirect('/showcart')

@login_required
def showcart(request):
	if request.user.is_authenticated:
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping = 70.0
		totalamount = 0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity*p.product.discount_prize)
				amount += tempamount
				totalamount = (amount+shipping)
			return render(request,'app/addtocart.html',{'carts':cart, 'amount':amount, 'totalamount':totalamount})
		return render(request, 'app/empty.html')

def plus_cart(request):
	if request.method == "GET":
		prod_id = request.GET['prod_id']
		print(prod_id)
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity += 1
		c.save()
		amount = 0.0
		shipping = 70.0
		totalamount = 0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity*p.product.discount_prize)
				amount += tempamount
				
			data = {
			 'quantity':c.quantity,
			 'amount' : amount,
			 'totalamount':amount+shipping,
			}
			return JsonResponse(data)

def minus_cart(request):
	if request.method == "GET":
		prod_id = request.GET['prod_id']
		print(prod_id)
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity -= 1
		c.save()
		amount = 0.0
		shipping = 70.0
		totalamount = 0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity*p.product.discount_prize)
				amount += tempamount
				
			data = {
			 'quantity':c.quantity,
			 'amount' : amount,
			 'totalamount':amount+shipping,
			}
			return JsonResponse(data)

def remove_cart(request):
	if request.method == "GET":
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping = 70.0
		totalamount = 0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity*p.product.discount_prize)
			amount += tempamount				
		data = {
		 'amount' : amount,
		 'totalamount':amount+shipping,
		}
		return JsonResponse(data)

def buy_now(request):

	return render(request,'app/buy_now.html')	

@method_decorator(login_required,name='dispatch')
class CustomerProfile(View):
	def get(self,request):
		form = CustomerProfileForm()
		return render(request, 'app/profile.html',{'form':form, 'active': 'btn-primary'})

	def post(self,request):
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
			reg.save()
			messages.success(request,'Congratlations !! Profile Updated Successfully')
		return render(request, 'app/profile.html',{'form':form, 'active': 'btn-primary'})

@login_required
def address(request):
	add = Customer.objects.filter(user=request.user)
	return render(request,'app/address.html',{'add':add, 'active': 'btn-primary'})

@login_required	
def orders(request):
	user = request.user
	order = Orderplaced.objects.filter(user=user)
	if order:
		return render(request,'app/orders.html',{'orders':order })
	return render(request,'app/emptyorders.html')

    

def mobile(request, data=None):
	if data == None:
		mobiles = Product.objects.filter(category='M')
	elif data == 'Samsung' or data == 'Redmi' or data == 'OnePlus':
		mobiles = Product.objects.filter(category='M').filter(brand=data)
	elif data == 'below':
		mobiles = Product.objects.filter(category='M').filter(discount_prize__lt=10000)
	elif data == 'above':
		mobiles = Product.objects.filter(category='M').filter(discount_prize__gt=10000)
	return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request, data=None):
	if data == None:
		laptops = Product.objects.filter(category='L')
	elif data == 'Asus' or data == 'HP':
		laptops = Product.objects.filter(category='L').filter(brand=data)
	return render(request, 'app/laptop.html',{'laptops':laptops})

def topwear(request, data=None):
	if data == None:
		topwears = Product.objects.filter(category='TW')
	elif data == 'Park' or data == 'Polo':
		topwears = Product.objects.filter(category='TW').filter(brand=data)
	return render(request, 'app/topwear.html',{'topwears':topwears})

def bottomwear(request, data=None):
	if data == None:
		bottomwears = Product.objects.filter(category='BW')
	elif data == 'Lee' or data == 'Spykar':
		bottomwears = Product.objects.filter(category='BW').filter(brand=data)
	return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})



class customerregistration(View):
	def get(self,request):
		form = UserRegistrationForm()
		return render(request, 'app/customerregistration.html',{'form':form})

	def post(self,request):
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			messages.success(request,'Congratlations !! Registered Successfully')
			form.save()
		return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_item = Cart.objects.filter(user=user)
	amount = 0.0
	shipping = 70.0
	totalamount = 0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity*p.product.discount_prize)
			amount += tempamount
		totalamount = amount+shipping
		return render(request,'app/checkout.html',{'add':add,'cart_item':cart_item,'totalamount':totalamount})

@login_required		
def paymentdone(request):
	user = request.user
	custid = request.GET.get('custid')
	customer =  Customer.objects.get(id=custid)
	cart = Cart.objects.filter(user=user)
	for c in cart:
		Orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
		c.delete()
	return redirect ('/orders')

@login_required	
@staff_member_required(login_url='/')
def AllProduct(request):
	product = Product.objects.all()
	return render(request,'app/viewproduct.html',{'product':product})



@method_decorator(staff_member_required(login_url='/'),name='dispatch')
class AddProduct(View):
	def get(self,request):
		form = ProductCreateForm()
		return render(request, 'app/addproduct.html',{'form':form})

	def post(self,request):
		form = ProductCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request,'Congratlations !! Your product Successfully added.')
			return redirect('/addproduct')
		return render(request, 'app/addproduct.html',{'form':form})

@login_required
@staff_member_required(login_url='/')
def UpdateData(request,pk):
	product = Product.objects.get(id=pk)
	print(product)
	form = ProductCreateForm(instance=product)
	if request.method == 'POST':
		form = ProductCreateForm(request.POST,request.FILES,instance=product)
		if form.is_valid():
			form.save()
			messages.success(request,'Congratlations !! Your product Successfully updated.')
		else:
			print(form.errors)
	return render(request,'app/addproduct.html',{'form':form })

@login_required
@staff_member_required(login_url='/')
def Delete(request,pk):
	product = Product.objects.get(id=pk)
	return render(request,'app/delete.html',{'product':product})

@login_required
@staff_member_required(login_url='/')
def ConfirmDelete(request,pk):
	product = Product.objects.get(id=pk)
	product.delete()
	return redirect('/allproduct')

@login_required
@staff_member_required(login_url='/')
def AllOrders(request):
	order = Orderplaced.objects.all()
	return render(request,'app/allorders.html',{'orders':order})

@login_required
@staff_member_required(login_url='/')
def OrderUpdate(request,pk):
	order_update = Orderplaced.objects.get(id=pk)
	form = OrderUpdateForm(instance=order_update)
	if request.method == 'POST':
		form = OrderUpdateForm(request.POST,instance=order_update)
		if form.is_valid():
			form.save()
			messages.success(request,'Successfully Updated !!')
		else:
			print(form.errors)
		return render(request,'app/updateorder.html',{'form':form})
	return render(request,'app/updateorder.html',{'form':form})

@login_required
@staff_member_required(login_url='/')
def RemoveOrder(request,pk):
	order_remove = Orderplaced.objects.get(id=pk)
	order_remove.delete()
	return redirect('/allorders')
