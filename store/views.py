from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User as p
from django.http import JsonResponse, HttpResponse
from .forms import ShippingForm, CreateUserForm, PortfolioForm
from ipware import get_client_ip
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import socket, datetime, os, json, random
from .utils import minfunc



## get another ip of same user (2 IPs in total from same user)
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]





def product_details(request, slug):
    data = minfunc(request)
    total_items = data['total_items']

    product = Product.objects.get(link=slug)
    products = Product.objects.all()
    prd_images = ProductImage.objects.filter(product=product)
    empfehlungen = random.sample(list(products), 10)
    if product in empfehlungen:
        empfehlungen.remove(product)
    var = 'sent'
    if 'color_code' in request.session:
        color = request.session['color_code']
        del request.session['color_code']
    else:
        color = '#00c300f5'
    return render(request, 'store/product_details.html',
                  {'total_items': total_items, 'empfehlungen': empfehlungen, 'product': product, 'prd_images': prd_images, 'var': var, 'color': color})

def products(request):
    data = minfunc(request)
    total_items = data['total_items']
    products = Product.objects.all()[:8]
    similar_products = Product.objects.all()[8:]
    var = 'sent'
    if 'color_code' in request.session:
        color = request.session['color_code']
        del request.session['color_code']
    else:
        color = '#00c300f5'
    return render(request, 'store/products.html', {'products': products, 'var': var, 'color': color,
                                                   'total_items': total_items, 'similar_products': similar_products})

def portfolio(request):
    ip, is_routable = get_client_ip(request)
    var = None
    if not ip:
        ip = '0.0.0.0'
    if '127' in ip:
        ip = get_ip_address()
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
            customer = Customer.objects.create(name=ip, email=ip+'@gmail.com', ip=IP)
        if request.method == 'POST':
            if form.is_valid():
                Portfolio.objects.create(user=customer, name=request.POST['name'], email=request.POST['email'], message=request.POST['message'], ip=IP)
                var = 'sent'
                messages.success(request, f'Thank you "{str(request.POST["name"]).title()}", your message has been sent successfully!')
                return render(request, 'store/portfolio.html', {'var': var})
            else:
                messages.error(request, 'Please fill all required fields')
    return render(request, 'store/portfolio.html', {'var': var})

def cart(request):
    data = minfunc(request)
    items = data['items']
    total_items = data['total_items']
    total = data['total']
    var = 'sent'
    if 'color_code' in request.session:
        color = request.session['color_code']
        del request.session['color_code']
    else:
        color = '#00c300f5'
    return render(request, 'store/cart.html', {'items': items, 'total': total, 'total_items': total_items, 'var': var, 'color': color})

def checkout(request):
    total, total_items = 0, 0
    form = ShippingForm(request.POST or None)
    var = 'sent'
    if 'color_code' in request.session:
        color = request.session['color_code']
        del request.session['color_code']
    else:
        color = '#00c300f5'
    if request.user.is_authenticated:
        customer = request.user.customer
        id_customer = customer.id
        try:
            order, created = Order.objects.get_or_create(customer=customer)
        except:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.filter(to_order=False)
        #return to store if user has no item in cart
        if items.count() < 1:
            request.session['color_code'] = '#f10000'
            messages.error(request, 'Sie haben noch kein Produkt in Ihren Warenkorb gelegt!')
            return redirect('store')
        for item in items:
            total = total + float(item.quantity_price())
        for item in items:
            total_items = total_items + item.quantity
        if request.method == 'POST':
            if form.is_valid():
                update = Customer(id=id_customer, name=request.POST['name'], email=request.POST['email'])
                update.save(update_fields=["name", "email"])
                ShippingAdress.objects.create(customer=customer, order=order, phone=request.POST['phone'], address=request.POST['address'],
                                              state=request.POST['state'], zipcode=request.POST['zipcode'])
                order.complete = True
                order.transaction_id = datetime.datetime.now().timestamp()
                order.save()
                for i in items:
                    i.to_order = True
                    i.save()
                messages.error(request, f'Vielen Dank {request.POST["name"].title()}, Ihre Bestellung wurde erfolgreich eingestellt, wir werden Sie bald kontaktieren')
                return redirect('store')
            else:
                color = '#b7e961'
                messages.error(request, 'Bitte füllen Sie alle erforderlichen Felder mit den richtigen Informationen aus')
        else:
            color = '#05a100'
            var = 'stop'
            messages.info(request, 'Ich habe die Zahlung auf dieser Seite nicht integriert, damit Sie den Checkout-Prozess testen können, PS: Sie können nicht in Zahlungsfelder schreiben')
    else:
        ip, is_routable = get_client_ip(request)
        if not ip:
            ip = '0.0.0.0'
        if '127' in ip:
            ip = get_ip_address()
        IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=ip, email=ip+'@gmail.com', ip=IP)
        try:
            order, created = Order.objects.get_or_create(customer=customer)
        except:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.filter(to_order=False)
        #return to store if user has no item in cart
        if items.count() < 1:
            request.session['color_code'] = '#f10000'
            messages.error(request, 'Sie haben noch kein Produkt in Ihren Warenkorb gelegt!')
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
                ShippingAdress.objects.create(customer=customer, phone=request.POST['phone'], address=request.POST['address'],
                                              state=request.POST['state'], zipcode=request.POST['zipcode'])
                order.complete = True
                transaction_id = datetime.datetime.now().timestamp()
                order.transaction_id = transaction_id
                order.save()
                for i in items:
                    i.to_order = True
                    i.save()
                messages.error(request, f'Vielen Dank {request.POST["name"].title()}, Ihre Bestellung wurde erfolgreich eingestellt, wir werden Sie bald kontaktieren')
                return redirect('store')
            else:
                color = '#b7e961'
                messages.error(request, 'Bitte füllen Sie alle erforderlichen Felder mit den richtigen Informationen aus')
        else:
            color = '#05a100'
            var = 'stop'
            messages.info(request, 'Ich habe die Zahlung auf dieser Seite nicht integriert, damit Sie den Checkout-Prozess testen können, PS: Sie können nicht in Zahlungsfelder schreiben')
    return render(request, 'store/checkout.html', {'items': items, 'customer': customer, 'total': total, 'total_items': total_items, 'form': form, 'var': var, 'color': color})



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
        if '127' in ip:
            ip = get_ip_address()
        IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=ip, email=ip+'@gmail.com', ip=IP)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        messages.info(request, f'"{item.product}" wurde zu Ihrem Warenkorb hinzugefügt')
        item.quantity = item.quantity + 1
    elif action == 'remove':
        messages.info(request, f'Sie verringern die Menge an "{item.product}"')
        item.quantity = item.quantity - 1
    item.save()
    if item.quantity <= 0:
        messages.info(request, f'"{item.product}" wurde erfolgreich gelöscht')
        item.delete()
    return JsonResponse('Item was added', safe=False)

def delete_item(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        ip, is_routable = get_client_ip(request)
        if not ip:
            ip = '0.0.0.0'
        if '127' in ip:
            ip = get_ip_address()
        IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=ip, email=ip+'@gmail.com', ip=IP)
    product = Product.objects.get(id=id)
    order = Order.objects.get(customer=customer, complete=False)
    item = OrderItem.objects.get(order=order, product=product, to_order=False)
    item.delete()
    return redirect('cart')

def register(request):
    if request.user.is_authenticated:
        request.session['color_code'] = '#b7e961'
        messages.info(request, f'Sie sind bereits eingeloggt')
        return redirect('store')
    else:
        form = CreateUserForm()
        data = minfunc(request)
        total_items = data['total_items']
        var = 'sent'
        if 'color_code' in request.session:
            color = request.session['color_code']
            del request.session['color_code']
        else:
            color = '#00c300f5'
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                ip, is_routable = get_client_ip(request)
                if not ip:
                    ip = '0.0.0.0'
                if '127' in ip:
                    ip = get_ip_address()
                IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
                email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                password = request.POST.get('password1')
                if User.objects.filter(email=email).exists():
                    request.session['color_code'] = '#b7e961'
                    messages.info(request, 'Konto existiert bereits mit dieser E-Mail! Bitte versuchen Sie sich anzumelden oder das Passwort zurückzusetzen')
                    return redirect('register')
                else:
                    user = form.save()
                # try get users who already have make an order
                try:
                    try:
                        customer = Customer.objects.get(email=email)
                    except:
                        customer = Customer.objects.get(email=ip+'@gmail.com')
                    if customer.user is not None:
                        # check if that user already have an account
                        request.session['color_code'] = '#b7e961'
                        messages.error(request, 'Konto existiert bereits mit dieser E-Mail! Bitte versuchen Sie sich anzumelden oder das Passwort zurückzusetzen')
                        return redirect('register')
                    else:
                        customer.user = user
                    customer.name = username
                    customer.email = email
                    if customer.ip == f'0.0.0.0||{str(request.META["HTTP_USER_AGENT"])}':
                        customer.ip = IP
                    customer.save()
                except:
                    Customer.objects.create(user=user, name=username, email=email, ip=IP)
                userlogin = authenticate(request, username=username, password=password)
                if userlogin is not None:
                    login(request, userlogin)
                    messages.success(request, f'Willkommen {username.title()}, Ihr Konto wurde erfolgreich erstellt ')
                else:
                    request.session['color_code'] = '#b7e961'
                    messages.info(request, 'Bitte loggen Sie sich ein!')
                    #send me email to contact the customer
                return redirect('store')
            else:
                request.session['color_code'] = '#b7e961'
                messages.error(request, 'Bitte füllen Sie alle erforderlichen Felder mit den richtigen Informationen aus')
        return render(request, 'auth/register.html', {'form': form, 'total_items': total_items, 'var': var, 'color': color})

def login_view(request):
    if request.user.is_authenticated:
        request.session['color_code'] = '#b7e961'
        messages.info(request, f'Sie sind bereits eingeloggt')
        return redirect('store')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = Customer.objects.get(email=email)
            except:
                messages.info(request, 'Username oder Password ist falsch')
                request.session['color_code'] = '#b7e961'
                return redirect('register')
            username = user.user.username
            auth = authenticate(request, username=username, password=password)
            if auth is None:
                messages.info(request, 'Username oder Password ist falsch')
                request.session['color_code'] = '#b7e961'
            else:
                login(request, auth)
                messages.info(request, f'Willkommen zurück {username.title()}')
                return redirect('store')
        return redirect('register')

@login_required(login_url='login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        request.session['color_code'] = '#b7e961'
        messages.info(request, "Sie haben noch kein konto!")
    return redirect('store')

def show_pdf(request):
    filepath = os.path.join('static', 'MouhcinPDF.pdf')
    fsock = open(filepath, "rb")
    response = HttpResponse(fsock, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Mouhcin-Qorra.pdf'
    # return FileResponse(open(filepath, 'rb'), content_type='application/pdf')   from django.http import FileResponse     for viewing only
    return response


