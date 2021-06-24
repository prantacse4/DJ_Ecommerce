from django.shortcuts import render, HttpResponseRedirect

from Order.models import *
from Ecom.models import *
from Product.models import *
from .forms import ContactForm

from django.db.models import Q
from django.shortcuts import redirect
from  django.contrib import messages
from django.db.models import Count
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    settings = Settings.objects.get(id=1)
    products = Product.objects.all()
    all_products = Product.objects.all()
    pc = products.count()
    categories = Category.objects.all().order_by('-id')
    latest_products = Product.objects.all().order_by('-id')
    companies = Company.objects.all().order_by('-id')


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
        'settings':settings,
        'products':products,
        'categories':categories,
        'latest_products':latest_products,
        'all_products':all_products,
        'total':total,
        'cartcount':cartcount,
        'companies':companies,
        }
    return render(request, 'Ecom/home.html', context = diction)



def contact(request):
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Your query is recorded')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    settings = Settings.objects.get(id=1)
    form = ContactForm()
    #Cart
    total = 0
    if request.user.is_authenticated:
        user = request.user
        mycarts = ShopCart.objects.filter(user = user)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty
    else:
        device = request.COOKIES['device']
        mycarts = ShopCartDevice.objects.filter(device=device)
        cartcount = mycarts.count()
        for p in mycarts:
            total = total+p.product.new_price*p.qty

    #Cart End
    diction = {
        'settings':settings,
        'form':form,
        'total':total,
        'cartcount':cartcount,
    }
    return render(request, 'Ecom/Contact.html', context = diction)