from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
#def home(request):
#return render(request, 'app/home.html')

class ProductView(View):
     def get(self, request):
       topwears = Product.objects.filter(category='TW')
       bottomwears = Product.objects.filter(category='BW')
       return render(request, 'app/home.html',
       {'topwears':topwears, 'bottomwears':bottomwears})

#def product_detail(request):
#return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',
        {'product':product})

def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount=0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
       
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount += 0.0
        shipping_amount = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount':totalamount 
            }
            return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

#def customerregistration(request):
#return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
        
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
         messages.success(request,'Congratualations!! Registered Succesfully')
        form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

def checkout(request):
 return render(request, 'app/checkout.html')
