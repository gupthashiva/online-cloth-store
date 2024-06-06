from django.shortcuts import render,redirect,HttpResponseRedirect
from myApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min
#from cart.cart import Cart
from django.views import View
from django.contrib.auth.hashers import  check_password
from django.http import HttpResponse
from myApp.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from myApp.forms import *
from decimal import Decimal
import razorpay
from django.conf import settings
# Create your views here.
def BASE(request):
  return render(request, 'base.html')

class HOME(View):
  def post(self, request):
        product = request.POST.get("product")
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart

        print(request.session['cart'])
        return redirect('cart')

    
  def get(self,request ):
    cart=request.session.get('cart')
    if not cart:
      request.session['cart']={}
      
    slider = Slider.objects.all().order_by('-id')[0:3]
    banner = Banner_Area.objects.all()
    main_category = Main_Category.objects.all().order_by('-id')
    product = Product.objects.filter(section__name="Top Deals Of The Day")
    products = Product.objects.all()
    #user session access
    print('you are :',request.session.get('email'))
    
    return render(request, 'main/home.html', locals())


#new product detail function 
def Product_Detail(request ,slug):
      product = Product.objects.get(slug=slug)
      product = Product.objects.filter(slug=slug)
      if product.exists():
        product = Product.objects.get(slug=slug)
        
      else:
        return redirect('404')
      return render(request, 'product/product_detail.html', locals() )

def Error404(request):
  return render(request, 'errors/404.html')

def My_Account(request):
  return render(request, 'registration/login.html')

def Register(request):
  if request.method=='POST':
      username = request.POST.get('username')
      email = request.POST.get('email')
      password = request.POST.get('password') 
      
      if User.objects.filter(username = username).exists():
        messages.error(request, 'user username already exists')
        return redirect('login')
      
      if User.objects.filter(email = email).exists():
        messages.error(request, 'user email already exists')
        return redirect('login')
      
      if User.objects.filter(password = password).exists():
        messages.error(request, 'user password already exists')
        return redirect('login')
      
      user = User.objects.create_user(username = username, email = email, password = password)
      user.set_password(password)
      user.save()
      
      return redirect('login')
    
  return render(request, 'registration/login.html')




def Login(request):
  
  if request.method =='POST':
     email = request.POST.get('email')
     username= request.POST.get('username')
     password = request.POST.get('password')
     #customer = User.get_customer_by_email(email)
     #customer = User.objects.get(email=email)
     
     user = authenticate(request, username=username, password=password, email=email)
     if user is not None:
        login(request,user)
        
        
        request.session['customer_id']=user.id
        request.session['email']=user.email
        
        if user:
            flag = check_password(password, user.password)
            if flag:
              request.session['customer'] = user.id
               
        return redirect('home')
      
     else:
      messages.error(request, 'Login failed. Please check your credentials.')
      return redirect('my_account')
    
  return render(request, 'registration/login.html')

  #return render(request, 'accounts/my_account.html')

@login_required(login_url='login')
def Profile(request):
  return render(request, 'profile/profile.html')

@login_required(login_url='login')
def Profile_Update(request):
  
  if request.method=='POST':
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user_id = request.user.id
    
    user = User.objects.get(id = user_id)
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = password
    
    if password != None and password != "":
       user.set_password(password)
    user.save()
    messages.success(request, 'your profile is successfully updated..')
    return redirect('profile')
  return render(request, 'profile/Profile_Update.html')


def About(request):
  return render(request, 'main/about.html')

def Contact(request):
  return render(request, 'main/contact.html')

def Products(request):
  category = Category.objects.all()
  product = Product.objects.all()
  color = Color.objects.all()
  brand = Brand.objects.all()
  
  min_price = Product.objects.all().aggregate(Min('price'))
  max_price = Product.objects.all().aggregate(Max('price'))
  print(min_price)
  print(max_price)
  
  color_id = request.GET.get('colorId')
  FilterPrice = request.GET.get('FilterPrice')
  
  if FilterPrice:
    Int_FilterPrice = int(FilterPrice)
    product = Product.objects.filter(price__lte = Int_FilterPrice)
    
  elif color_id:
     product= Product.objects.filter(color=color_id)
     #product= Product.objects.filter(color=color_id)
  else:
    product = Product.objects.all()
  
  return render(request, 'main/product.html', locals())

def Filter_Data(request):
    category_ids = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all()

    if len(category_ids) > 0:
        allProducts = allProducts.filter(categories__id__in=category_ids).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()

    rendered_template = render_to_string('ajax/product.html', {'product': allProducts})
    
    return JsonResponse({'data': rendered_template})


#add to cart 
def calculate_total_price(cart):
    total_price = 0
    for item_id, quantity in cart.items():
        # Assuming you have a Product model with a price field
        product = Product.objects.get(id=item_id)
        total_price += product.price * quantity
    return total_price

def calculate_total_price(cart):
    total_price = 0
    for item_id, quantity in cart.items():
        # Assuming you have a Product model with a price field
        product = Product.objects.get(id=item_id)
        total_price += product.price * quantity
    
    # Calculate 50% discount
    discount_amount = total_price * 0.5
    
    # Apply discount
    total_price -= discount_amount
    
    return total_price


def Cart(request):
    products = Product.objects.all()
    
    cart = request.session.get('cart', {})
    
    total_price = calculate_total_price(cart)
    discount_amount = total_price * 0.5
    discounted_total_price = total_price - discount_amount
    
  
    return render(request, 'cart/cart.html', locals())
  

def Check_Out(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        customer = request.session.get('customer')
        cart = request.session.get('cart', {})
        product_ids = [int(pid) for pid in cart.keys() if pid.isdigit()]  # Filter out non-numeric keys
        if not product_ids:
            return HttpResponse("Cart is empty.")
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            quantity = cart.get(str(product.id), 0)
            if quantity > 0:
                order = Order.objects.create(
                    customer=User.objects.get(id=customer),
                    product=product,
                    price=product.price,
                    address=address,
                    phone=phone_number,
                    quantity=quantity
                )
        request.session['cart'] = {}
        return redirect("home")
    return render(request, 'cart/check_out.html')



''' 
def Check_Out(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        customer = request.session.get('customer')

        print(customer)

        # Assuming `cart` is a dictionary where keys are product IDs
        cart = request.session.get('cart')
        product_ids = list(cart.keys())
        products = Product.get_products_by_id(product_ids)

        print(address, phone_number, first_name, customer, cart, products)

        for product in products:
            if address:
                order = Order(
                    customer=User.objects.get(id=customer),
                    product=product,
                    price=product.price,
                    address=address,
                    phone=phone_number,
                    quantity=cart.get(str(product.id))
                )
                order.Place_Order()

            else:
                return HttpResponse("Address is required.")
        
        request.session['cart'] = {}  # Clear the cart after placing orders
        return redirect("home")
    
    return render(request, 'cart/check_out.html')'''

# if u have 2 args using  @method_decorator(auth_middleware)
#@method_decorator(auth_middleware)


#@auth_middleware
def Orders(request):
  customer = request.session.get('customer')
  orders = Order.get_orders_by_cutomer(customer)
  print(orders, customer)
  
  return render(request, 'cart/orders.html', locals() )

def Item_Clear(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart: 
      del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')


def payment_get_way(request):
  
  if request.method=='POST':
    name = request.POST.get('name')
    amount = int(request.POST.get('amount'))*100
    
    # authorize razorpay client with API Keys.
    client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    #create order
    response_payment=client.order.create(dict(amount=amount,currency='INR'))
    
    order_id = response_payment['id']
    order_status= response_payment['status']
    
    if order_status=='created':
      payment_get_way = Payment_Get_Way(name=name,amount=amount,order_id=order_id)
      payment_get_way.save()
      response_payment['name'] = name
      
      form=Payment_Get_Way_Form(request.POST or None)
      return render(request,'cart/payment_get_way.html', {'form':form, 'payment':response_payment})
    
  form=Payment_Get_Way_Form()
  
  return render(request,'cart/payment_get_way.html', locals())

def payment_status(request):
  response = request.POST
  params_dict={
              'razorpay_order_id':response['razorpay_order_id'],

              'razorpay_payment_id':response['razorpay_payment_id'],
              'razorpay_signature':response['razorpay_signature'], 
                
                } 
  
  # authorize razorpay client with API Keys.
  client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
  try:
      status = client.utility.verify_payment_signature(params_dict)
      payment_get_way = Payment_Get_Way.objects.get(order_id=response['razorpay_order_id'])
      payment_get_way.razorpay_payment_id = response['razorpay_payment_id']
      payment_get_way.paid= True
      payment_get_way.save()
      return render(request,'cart/payment_status.html', {'status':True})
      
  except:
  
      return render(request,'cart/payment_status.html', {'status':False})
  
  return render(request,'cart/payment_status.html')