from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from .forms import UserRegistrationForm
from django.contrib import messages
from .filters import ProductFilter
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required

def store(request):

    data = cartData(request)

    cartItems = data['cartItems']

    products=Product.objects.all()



    myFilter = ProductFilter(request.GET,queryset=products)
    products = myFilter.qs

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context={'products':products,'cartItems':cartItems,'myFilter':myFilter}
    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)

def checkout(request):
    data=cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)

def updateitem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('ProductId:',productId)
    print('Action:',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added',safe=False)


def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)



    else:
        customer,order=guestOrder(request,data)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )


    return JsonResponse('Payment Complete..',safe=False)


def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data.get('username')
            form.save()
            messages.success(request,f'Account Created successfully for {u}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'store/register.html',{'form':form})

@login_required(login_url='login')
def previousOrders(request):
    cur_user=request.user
    cur_cust=Customer.objects.filter(user=cur_user).first()
    cur_cust_orders=Order.objects.filter(customer=cur_cust)

    all_order_details=[]

    for order in cur_cust_orders:
        all_order_items=OrderItem.objects.filter(order=order)
        all_product_details=[]
        for orderItem in all_order_items:
            temp={'product_name':orderItem.product.name,
                  'product_image':orderItem.product.image,
                  'product_price':orderItem.product.price,
                  'product_quantity':orderItem.quantity}
            all_product_details.append(temp)
        qwe={'order':order,'details':all_product_details}
        all_order_details.append(qwe)

    context={
        'all_order_details':all_order_details,
    }
    return render(request,'store/my_orders.html',context)


