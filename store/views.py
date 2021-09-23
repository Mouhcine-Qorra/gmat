from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User as p
from django.http import JsonResponse, HttpResponse
from .forms import ShippingForm, CreateUserForm, PortfolioForm
from ipware import get_client_ip
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime, os, json
from .filters import ProductFilter
from .utils import minfunc



## get another ip of same user (2 IPs in total from same user)
#def get_ip_address():
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s.connect(("8.8.8.8", 80))
#    return s.getsockname()[0]





def product_details(request):
    return render(request, 'store/product_details.html')

def products(request):
    return render(request, 'store/products.html')

def portfolio(request):
    ip, is_routable = get_client_ip(request)
    var = None
    if not ip:
        ip = '0.0.0.0'
    IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
    form = PortfolioForm(request.POST or None)
    if request.user.is_authenticated:
        customer = request.user.customer
        if request.method == 'POST':
            if form.is_valid():
                Portfolio.objects.create(user=customer, name=request.POST['name'], email=request.POST['email'], message=request.POST['message'], ip=IP)
                messages.success(request, f'Thank you {str(request.POST["name"]).title()}, your message has been sent successfully!')
                var = 'sent'
                return render(request, 'store/portfolio.html', {'var': var})
            else:
                messages.error(request, 'Please fill all required fields')
    else:
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=IP, email=IP+'@gmail.com', ip=IP)
        if request.method == 'POST':
            if form.is_valid():
                Portfolio.objects.create(user=customer, name=request.POST['name'], email=request.POST['email'], message=request.POST['message'], ip=IP)
                var = 'sent'
                messages.success(request, f'Thank you "{str(request.POST["name"]).title()}", your message has been sent successfully!')
                return render(request, 'store/portfolio.html', {'var': var})
            else:
                messages.error(request, 'Please fill all required fields')
    return render(request, 'store/portfolio.html', {'var': var})

def store(request):
    data = minfunc(request)
    total_items = data['total_items']
    products = Product.objects.all()
    myfilter = ProductFilter(request.GET, queryset=products)
    products = myfilter.qs
    return render(request, 'store/store.html', {'products': products, 'total_items': total_items, 'filter': myfilter})

def cart(request):
    data = minfunc(request)
    items = data['items']
    total_items = data['total_items']
    total = data['total']
    return render(request, 'store/cart.html', {'items': items, 'total': total, 'total_items': total_items})

def checkout(request):
    total, total_items = 0, 0
    form = ShippingForm(request.POST or None)
    if request.user.is_authenticated:
        customer = request.user.customer
        id_customer = customer.id
        try:
            order, created = Order.objects.get_or_create(customer=customer)
        except:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.filter(is_current=True)
        if items.count() < 1:
            return redirect('store')
        for item in items:
            total = total + float(item.quantity_price())
        for item in items:
            total_items = total_items + item.quantity
        if request.method == 'POST':
            if form.is_valid():
                update = Customer(id=id_customer, name=request.POST['name'], email=request.POST['email'])
                update.save(update_fields=["name", "email"])
                ShippingAdress.objects.create(customer=customer, order=order, address=request.POST['address'],
                                              city=request.POST['city'], zipcode=request.POST['zipcode'])
                order.complete = True
                transaction_id = datetime.datetime.now().timestamp()
                order.transaction_id = transaction_id
                order.save()
                for i in items:
                    i.is_current = False
                    i.save()
                return redirect('store')
            else:
                messages.error(request, 'Please fill all required fields')
    else:
        ip, is_routable = get_client_ip(request)
        if not ip:
            ip = '0.0.0.0'
        IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=ip, email=IP+'@gmail.com', ip=IP)
        try:
            order, created = Order.objects.get_or_create(customer=customer)
        except:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.filter(is_current=True)
        if items.count() < 1:
            return redirect('store')
        id_customer = customer.id
        for item in items:
            total = total + float(item.quantity_price())
        for item in items:
            total_items = total_items + item.quantity
        if request.method == 'POST':
            if form.is_valid():
                update = Customer(id=id_customer, name=request.POST['name'], email=request.POST['email'])
                update.save(update_fields=["name", "email"])
                ShippingAdress.objects.create(customer=customer, order=order, address=request.POST['address'],
                                              city=request.POST['city'], zipcode=request.POST['zipcode'])
                order.complete = True
                transaction_id = datetime.datetime.now().timestamp()
                order.transaction_id = transaction_id
                order.save()
                for i in items:
                    i.is_current = False
                    i.save()
                return redirect('store')
            else:
                messages.error(request, 'Please fill all required fields')
    return render(request, 'store/checkout.html', {'items': items, 'customer': customer, 'total': total, 'total_items': total_items, 'form': form})



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    user = data['user']
    if user != 'AnonymousUser':
        user_inf = p.objects.get(username=user)
        customer = Customer.objects.get(user=user_inf)
    else:
        ip, is_routable = get_client_ip(request)
        if not ip:
            ip = '0.0.0.0'
        IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=IP, email=IP+'@gmail.com', ip=IP)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        item.quantity = item.quantity + 1
    elif action == 'remove':
        item.quantity = item.quantity - 1
    item.save()
    if item.quantity <= 0:
        item.delete()
    return JsonResponse('Item was added', safe=False)

def delete_item(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        ip, is_routable = get_client_ip(request)
        if not ip:
            ip = '0.0.0.0'
        IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=IP, email=IP+'@gmail.com', ip=IP)
    product = Product.objects.get(id=id)
    order = Order.objects.get(customer=customer, complete=False)
    item = OrderItem.objects.get(order=order, product=product, is_current=True)
    item.delete()
    return redirect('cart')

def register(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                ip, is_routable = get_client_ip(request)
                if not ip:
                    ip = '0.0.0.0'
                IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
                email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                password = request.POST.get('password1')
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'User with this email already exist! try to login')
                    return redirect('login')
                else:
                    user = form.save()
                # try get users who already have make an order
                try:
                    try:
                        customer = Customer.objects.get(email=email)
                    except:
                        customer = Customer.objects.get(email=IP+'@gmail.com')
                    if customer.user is not None:
                        # check if that user already have an account
                        messages.error(request, 'account already exist with this email! please try to login or reset password')
                        return render(request, 'auth/login.html', {'form': form})
                    else:
                        customer.user = user
                    customer.name = username
                    customer.email = email
                    if customer.ip == f'0.0.0.0||{str(request.META["HTTP_USER_AGENT"])}':
                        customer.ip = IP
                    customer.save()
                    print(f'\n\ndaz mn try')
                except:
                    Customer.objects.create(user=user, name=username, email=email, ip=IP)
                    print(f'\n\ndaz mn except')
                userlogin = authenticate(request, username=username, password=password)
                if userlogin is not None:
                    login(request, userlogin)
                    messages.success(request, f'Welcome {username.title()}, your account has been created successfully ')
                else:
                    messages.info(request, 'Account already exist!')
                return redirect('store')
            else:
                messages.error(request, 'please fill all fields with correct informations')
        return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        msg = None
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = Customer.objects.get(email=email)
            except:
                messages.info(request, 'Username or Password is incorrect')
                msg = 'info'
                return render(request, 'auth/login.html', {'msg': msg})
            username = user.user.username
            auth = authenticate(request, username=username, password=password)
            if auth is None:
                msg = 'info'
            else:
                login(request, auth)
                return redirect('store')
        return render(request, 'auth/login.html', {'msg': msg})

@login_required(login_url='login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "you dont have an account yet!")
    return redirect('store')

def show_pdf(request):
    filepath = os.path.join('static', 'MouhcinPDF.pdf')
    fsock = open(filepath, "rb")
    response = HttpResponse(fsock, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Mouhcin-Qorra.pdf'
    # return FileResponse(open(filepath, 'rb'), content_type='application/pdf')   from django.http import FileResponse     for viewing only
    return response


