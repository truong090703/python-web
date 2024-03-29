from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    context = {'form':form}
    return render(request, 'app/register.html', context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: messages.info(request,'Tên tài khoản hoặc mật khẩu sai')

    context = {}
    return render(request, 'app/login.html', context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Không đăng nhập, đặt order là None hoặc giá trị mặc định
        order = None
        items = []
        cartItems = 0

    products = Product.objects.all()
    context = {'products': products, 'cartItem': cartItems}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'order.get_cart_items': 0, 'order.get_cart_total': 0}
        cartItems = order.get_cart_items

    context={'items': items, 'order': order, 'cartItem': cartItems}
    return render(request, 'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'order.get_cart_items': 0, 'order.get_cart_total': 0}
        cartItems = order.get_cart_items

    context={'items': items, 'order': order, 'cartItem': cartItems}
    return render(request, 'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
def deleteItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productId = data['productId']
        customer = request.user
        try:
            order = Order.objects.get(customer=customer, complete=False)
            orderItem = OrderItem.objects.get(order=order, product_id=productId)
            orderItem.delete()
            return JsonResponse({'message': 'Item deleted successfully'}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order does not exist'}, status=404)
        except OrderItem.DoesNotExist:
            return JsonResponse({'error': 'Item does not exist in the cart'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
def product(request):
    query = request.GET.get('searched')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query))

    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

    context = {'products': products, 'cartItem': cartItems}
    return render(request, 'app/product.html', context)
def profile(request):
    cartItems = 0
    if request.user.is_authenticated:
        user = request.user
        username = user.username
        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        order = Order.objects.get_or_create(customer=user, complete=False)[0]  # Lấy hoặc tạo đơn hàng cho người dùng
        cartItems = order.get_cart_items  # Lấy số lượng sản phẩm trong giỏ hàng
        context = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'cartItem': cartItems  # Truyền cartItems vào context
        }
        return render(request, 'app/profile.html', context)
    else:
        return redirect('login')

