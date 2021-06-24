from django.shortcuts import render, HttpResponseRedirect
from Order.models import *
from Ecom.models import *
from accounts.models import *
from Product.models import *
from .forms import ShoppingCartForm, ShoppingCartDeviceForm, OderForm, ShoppingCartUpdateDeviceForm

from django.db.models import Q
from django.shortcuts import redirect
from  django.contrib import messages
from django.db.models import Count
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
# Create your views here.


def add_to_wishlist(request, id):
    if request.user.is_authenticated == False:
        messages.success(request, 'Please login to add items on your wishlist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    user = request.user
    avail = Wishlist.objects.filter(product_id = id)
    if avail:
        #remove
        data = Wishlist.objects.get(product_id=id, user=user)
        data.delete()
        messages.success(request, 'Item removed to your wishlist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        #create
        data = Wishlist.objects.create(product_id=id, user=user)
        data.save()
        messages.success(request, 'Item added to your wishlist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login_user')
def mywishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    categories = Category.objects.all().order_by('-id')
    settings = Settings.objects.get(id=1)
    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        try:
            device = request.COOKIES['device']
            mycarts = ShopCartDevice.objects.filter(device=device)
            cartcount = mycarts.count()
            for p in mycarts:
                total = total+p.product.new_price*p.qty
        except:
            total = 0
            cartcount = 0

    #Cart End
    diction = {
        'categories':categories,
        'settings':settings,
        'total':total,
        'cartcount':cartcount,
        'wishlist':wishlist,
    }
    return render(request, 'Ecom/MyWishlist.html', context=diction)

def add_to_cart(request, id):
    current_user = request.user
    device = request.COOKIES['device']
    if request.user.is_authenticated:
        checking = ShopCart.objects.filter(product_id = id, user_id = current_user.id)
        if checking:
            control = 1
        else:
            control = 0

        if request.method == "POST":
            form = ShoppingCartForm(request.POST)
            if form.is_valid():
                newqty = form.cleaned_data['qty']
                if control == 1:
                    data = ShopCart.objects.get(product_id = id, user_id = current_user.id)
                    data.qty = data.qty + newqty
                    data.save()
                else:
                    data = ShopCart()
                    data.user = current_user
                    data.product_id = id 
                    data.qty = newqty
                    data.save() 
            messages.success(request, 'Item added to your Cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:

            if control == 1:
                data = ShopCart.objects.get(product_id = id, user_id = current_user.id)
                data.qty += form.cleaned_data['qty']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id 
                data.qty = 1
                data.save() 
            messages.success(request, 'Item added to your Cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        checking = ShopCartDevice.objects.filter(product_id = id, device = device)
        if checking:
            control = 1
        else:
            control = 0

        if request.method == "POST":
            form = ShoppingCartDeviceForm(request.POST)
            if form.is_valid():
                newqty = form.cleaned_data['qty']
                if control == 1:
                    data = ShopCartDevice.objects.get(product_id = id, device = device)
                    data.qty = data.qty + newqty
                    data.save()
                else:
                    data = ShopCartDevice()
                    data.device = device
                    data.product_id = id 
                    data.qty = newqty
                    data.save() 
            messages.success(request, 'Item added to your Cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:

            if control == 1:
                data = ShopCartDevice.objects.get(product_id = id, device = device)
                data.qty += form.cleaned_data['qty']
                data.save()
            else:
                data = ShopCartDevice()
                data.device = device
                data.product_id = id 
                data.qty = 1
                data.save() 
            messages.success(request, 'Item added to your Cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def update_cart_qty(request, id):
    if request.user.is_authenticated:
        user = request.user
        cart_data = ShopCart.objects.get(id = id, user=user)
        if request.method == "POST":
            form = ShoppingCartForm(request.POST)
            newqty = request.POST.get('qty')
            cart_data.qty = newqty
            cart_data.save()
        messages.success(request, 'Cart Updated')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

    else:
        device = request.COOKIES['device']
        cart_data = ShopCartDevice.objects.get(id = id, device=device)
        if request.method == "POST":
            form = ShoppingCartUpdateDeviceForm(request.POST)
            newqty = request.POST.get('qty')
            cart_data.qty = newqty
            cart_data.save()
        messages.success(request, 'Cart Updated')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_details(request):
    current_user = request.user
    device = request.COOKIES['device']
    categories = Category.objects.all().order_by('-id')
    settings = Settings.objects.get(id=1)
    if current_user.is_authenticated:
        cart_products = ShopCart.objects.filter(user=current_user)
    else:
        cart_products = ShopCartDevice.objects.filter(device=device)

    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        try:
            device = request.COOKIES['device']
            mycarts = ShopCartDevice.objects.filter(device=device)
            cartcount = mycarts.count()
            for p in mycarts:
                total = total+p.product.new_price*p.qty
        except:
            total = 0
            cartcount = 0

    #Cart End
    total = total+100
    diction = {
        'categories':categories,
        'settings':settings,
        'cart_products':cart_products,
        'total':total,
        'cartcount':cartcount,
    }
    return render(request, 'Ecom/cart_details.html', context = diction)


def cart_delete(request, id):
    user = request.user
    device = request.COOKIES['device']
    if user.is_authenticated:
        cart_product = ShopCart.objects.filter(id = id, user=user)
    else:
        cart_product = ShopCartDevice.objects.filter(id = id,device=device)

    cart_product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





@login_required(login_url='login_user')
def CheckOut(request):
    
    current_user = request.user
    shoping_cart = ShopCart.objects.filter(user_id=current_user.id)
    sccount = shoping_cart.count()
    shipping = ShippingCharge.objects.all()
    shipcharge = 100
    if sccount == 0:
        messages.success(request, 'Your Cart is Empty')
        return redirect('home')
    totalamount = 0
    for rs in shoping_cart:
        totalamount += rs.qty*rs.product.new_price
    if request.method == "POST":
        form = OderForm(request.POST, request.FILES)
        if form.is_valid():
            dat = Order()
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id = current_user.id

            for ship in shipping:
                if ship.city == form.cleaned_data['city']:
                    shipcharge = ship.charge
            dat.total = totalamount+shipcharge
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper() 
            dat.code = ordercode
            dat.save()

            # moving data shortcart to product cart
            for rs in shoping_cart:
                data = OderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.qty = rs.qty
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.qty
                product.save()

            # Now remove all oder data from the shoping cart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            # request.session['cart_item']=0
            messages.success(request, 'Your oder has been completed')
            categories = Category.objects.all()
            settings = Settings.objects.get(id=1)

            #Cart
            total = 0
            if request.user.is_authenticated:
                user = request.user
                mycarts = ShopCart.objects.filter(user = user)
                cartcount = mycarts.count()
                for p in mycarts:
                    total = total+p.product.new_price*p.qty
            else:
                try:
                    device = request.COOKIES['device']
                    mycarts = ShopCartDevice.objects.filter(device=device)
                    cartcount = mycarts.count()
                    for p in mycarts:
                        total = total+p.product.new_price*p.qty
                except:
                    total = 0
                    cartcount = 0

            #Cart End
            diction = {
                # 'category':category,
                'ordercode': ordercode,
                'categories': categories,
                'settings': settings,
                'total':total,
                'cartcount':cartcount,
            }

            return render(request, 'Ecom/order_completed.html', context = diction)
        else:
            messages.warning(request, form.errors)
          #  return HttpResponseRedirect("/order/oder_cart")
    form = OderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    total_amount = 0
    for p in shoping_cart:
        total_amount += p.product.new_price*p.qty
    categories = Category.objects.all()
    settings = Settings.objects.get(id=1)

    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        try:
            device = request.COOKIES['device']
            mycarts = ShopCartDevice.objects.filter(device=device)
            cartcount = mycarts.count()
            for p in mycarts:
                total = total+p.product.new_price*p.qty
        except:
            total = 0
            cartcount = 0

    #Cart End
    diction = {
        # 'category':category,
        'shoping_cart': shoping_cart,
        'totalamount': totalamount,
        'profile': profile,
        'form': form,
        'categories': categories,
        'settings': settings,
        'total_amount': total_amount,
        'total':total,
        'cartcount':cartcount,
    }
    return render(request, 'Ecom/checkout.html', context = diction)


@login_required(login_url='login_user')
def Order_showing(request):
    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        try:
            device = request.COOKIES['device']
            mycarts = ShopCartDevice.objects.filter(device=device)
            cartcount = mycarts.count()
            for p in mycarts:
                total = total+p.product.new_price*p.qty
        except:
            total = 0
            cartcount = 0

    #Cart End
    categories = Category.objects.all()
    settings = Settings.objects.get(id=1)
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    diction = {
        'categories': categories,
        'settings': settings,
        'orders': orders,
        'total':total,
        'cartcount':cartcount,

    }

    return render(request, 'Ecom/user_order_showing.html', context = diction)



@login_required(login_url='login_user')
def user_order_details(request, id):
    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        try:
            device = request.COOKIES['device']
            mycarts = ShopCartDevice.objects.filter(device=device)
            cartcount = mycarts.count()
            for p in mycarts:
                total = total+p.product.new_price*p.qty
        except:
            total = 0
            cartcount = 0

    #Cart End
    categories = Category.objects.all()
    settings = Settings.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    order_products = OderProduct.objects.filter(order_id=id)
    diction = {

        'order': order,
        'order_products': order_products,
        'categories': categories,
        'settings': settings,
        'total':total,
        'cartcount':cartcount,
    }
    return render(request, 'Ecom/user_order_details.html', context = diction)




@login_required(login_url='login_user')
def Order_Product_showing(request):
    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        try:
            device = request.COOKIES['device']
            mycarts = ShopCartDevice.objects.filter(device=device)
            cartcount = mycarts.count()
            for p in mycarts:
                total = total+p.product.new_price*p.qty
        except:
            total = 0
            cartcount = 0

    #Cart End
    categories = Category.objects.all()
    settings = Settings.objects.get(id=1)
    current_user = request.user
    order_product = OderProduct.objects.filter(user_id=current_user.id)
    diction = {
        'categories': categories,
        'settings': settings,
        'order_product': order_product,
        'total':total,
        'cartcount':cartcount,

    }

    return render(request, 'Ecom/OrderProducList.html', context = diction)


@login_required(login_url='login_user')
def user_order_product_details(request, id, oid):
    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        try:
            device = request.COOKIES['device']
            mycarts = ShopCartDevice.objects.filter(device=device)
            cartcount = mycarts.count()
            for p in mycarts:
                total = total+p.product.new_price*p.qty
        except:
            total = 0
            cartcount = 0

    #Cart End
    categories = Category.objects.all()
    settings = Settings.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    order_products = OderProduct.objects.get(user_id=current_user.id, id=id)
    diction = {

        'order': order,
        'order_products': order_products,
        'categories': categories,
        'settings': settings,
        'total':total,
        'cartcount':cartcount,
    }
    return render(request, 'Ecom/user_order_pro_details.html', context = diction)