from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum, Avg, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from Product.models import *
from Ecom.models import *
from Order.models import *
from .forms import SearchForm, CommentForm
# Create your views here.


def single_product(request, id):
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
    comments = Comment.objects.filter(product_id=id, status=True)
    settings = Settings.objects.get(id=1)
    categories = Category.objects.all().order_by('-id')
    single_product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    pc = single_product.category
    all_products = Product.objects.filter(category=pc)
    products = Product.objects.all()
    companies = Company.objects.all()
    diction = {
        'settings':settings,
        'single_product':single_product,
        'categories':categories,
        'images':images,
        'all_products':all_products,
        'products':products,
        'total':total,
        'cartcount':cartcount,
        'companies':companies,
        'comments':comments,
    }
    return render(request, 'Ecom/single_product.html', context = diction)


def category_product(request, id, slug):
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
    settings = Settings.objects.get(id=1)
    categories = Category.objects.all().order_by('-id')
    companies = Company.objects.all().order_by('-id')
    cproducts = Product.objects.filter(category_id=id)
    all_products = Product.objects.all()
    this = Category.objects.get(id=id)
    pc = cproducts.count()
    latest_products = Product.objects.filter(category_id=id).order_by('-id')
    diction = {
        'settings':settings,
        'categories':categories,
        'cproducts':cproducts,
        'cproducts':cproducts,
        'latest_products':latest_products,
        'all_products':all_products,
        'total':total,
        'cartcount':cartcount,
        'this':this,
        'products':all_products,
        'companies':companies,
    }
    return render(request, 'Ecom/category_product.html', context = diction)
 

def searchproducts(request):
    settings = Settings.objects.get(id=1)
    categories = Category.objects.all().order_by('-id')
    products = Product.objects.all()
    companies = Company.objects.all()
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
    if request.method == "POST":
        
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(title__icontains=query)
            diction = {
                'settings':settings,
                'results':results,
                'products':products,
                'q':query,
                'total':total,
                'cartcount':cartcount,
                'categories':categories,
                'companies':companies
            }
            return render(request, 'Ecom/searchresults.html', context = diction)
    diction = {
        'settings':settings,
        'products':products,
        'total':total,
        'cartcount':cartcount,
        'categories':categories,
        'companies':companies
    }
    return render(request, 'Ecom/searchresults.html', context = diction)


def Comment_Add(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'Thanks for your comment')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))