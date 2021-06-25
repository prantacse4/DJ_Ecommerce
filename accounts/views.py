from django.shortcuts import render, HttpResponseRedirect

from Order.models import *
from Ecom.models import *
from Product.models import *
from accounts.models import *
from .forms import UserCreationForm, SignupForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from  django.contrib import messages
from django.db.models import Count
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.


def login_user(request):
    if(request.user.is_authenticated):
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = authenticate(request, username=User.objects.get(email=username), password=password)
                
            except:
                user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_superuser == True:
                    return HttpResponseRedirect('/admin')

                #adding cookies cart to the user data
                else:
                    device = request.COOKIES['device']
                    carts = ShopCartDevice.objects.filter(device=device)
                    for c in carts:
                        checkusercart = ShopCart.objects.filter(user=request.user, product = c.product)
                        if checkusercart:
                            data = ShopCart.objects.get(product_id = c.product.id, user_id = request.user.id)
                            data.qty = data.qty + c.qty
                            data.save()
                            devicecartdata = ShopCartDevice.objects.filter(device=device, product=c.product)
                            devicecartdata.delete()
                        else:
                            data = ShopCart()
                            data.user = request.user
                            data.product_id = c.product.id 
                            data.qty = c.qty
                            data.save() 
                            devicecartdata = ShopCartDevice.objects.filter(device=device, product=c.product)
                            devicecartdata.delete()
                            
                return redirect('home')
            
            else:
                messages.success(request, 'Incorrect Username or Password')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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

    diction = {

        'settings':settings,
        'total':total,
        'cartcount':cartcount,
    }
    return render(request, 'Ecom/user_signin.html', context=diction)




def signup_user(request):
    if(request.user.is_authenticated):
        return redirect('home')
    else:
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

        myform = SignupForm()
        if request.method == 'POST':
            myform = SignupForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password1')
            if myform.is_valid():
                myform.save(commit=True)
                newUser = User.objects.get(username=username)
                userdata = UserProfile.objects.create(user = newUser)
                userdata.save()   
                messages.success(request, 'Account Created for '+ username)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if request.user.is_superuser == True:
                        return HttpResponseRedirect('/admin')

                    #adding cookies cart to the user data
                    else:
                        device = request.COOKIES['device']
                        carts = ShopCartDevice.objects.filter(device=device)
                        for c in carts:
                            checkusercart = ShopCart.objects.filter(user=request.user, product = c.product)
                            if checkusercart:
                                data = ShopCart.objects.get(product_id = c.product.id, user_id = request.user.id)
                                data.qty = data.qty + c.qty
                                data.save()
                                devicecartdata = ShopCartDevice.objects.filter(device=device, product=c.product)
                                devicecartdata.delete()
                            else:
                                data = ShopCart()
                                data.user = request.user
                                data.product_id = c.product.id 
                                data.qty = c.qty
                                data.save() 
                                devicecartdata = ShopCartDevice.objects.filter(device=device, product=c.product)
                                devicecartdata.delete()
                                
                    return redirect('home')
            diction = {

            'settings':settings,
            'total':total,
            'cartcount':cartcount,
            'myform':myform,
                }
            return render(request, 'Ecom/signup_user.html', context = diction)

        diction = {

            'settings':settings,
            'total':total,
            'cartcount':cartcount,
            'myform':myform,
        }
        return render(request, 'Ecom/signup_user.html', context = diction)


@login_required(login_url='login_user')
def user_profile(request):
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        profile = UserProfile.objects.get(user=request.user)

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
    diction = {
        'profile':profile,
        'settings':settings,
        'total':total,
        'cartcount':cartcount,
    }

    return render(request, 'Ecom/user_profile.html', context=diction)


@login_required(login_url='login_user')
def user_update(request):
    profile = UserProfile.objects.get(user=request.user)
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
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_obj = UserProfile.objects.get(user=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('user_profile')
        
        diction = {
            'profile':profile,
            'settings':settings,
            'total':total,
            'cartcount':cartcount,
            'myform':user_form,
        }
        return render(request, 'Ecom/user_update.html', context = diction)
    
    else:


        diction = {
            'profile':profile,
            'settings':settings,
            'total':total,
            'cartcount':cartcount,
        }
        return render(request, 'Ecom/user_update.html', context = diction)


@login_required(login_url='login_user')
def change_password(request):

    profile = UserProfile.objects.get(user=request.user)
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

    if request.method == "POST":
        pass_form = PasswordChangeForm(request.user, request.POST)
        if pass_form.is_valid():
            user = pass_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your Password has successfully changed!')
            return redirect('user_update')
        else:
            messages.error(request, 'Please Correct the error.')
            diction = {
            'profile':profile,
            'settings':settings,
            'total':total,
            'cartcount':cartcount,
            'pass_form':pass_form,
            }
            return render(request, 'Ecom/change_password.html', context = diction)
    
    else:
        pass_form = PasswordChangeForm(request.user)
        diction = {
            'profile':profile,
            'settings':settings,
            'total':total,
            'cartcount':cartcount,
            'pass_form':pass_form,
        }
        return render(request, 'Ecom/change_password.html', context = diction)


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('home')




@login_required(login_url='login_user')
def user_comment(request):
    categories = Category.objects.all()
    settings = Settings.objects.get(id=1)
    current_user = request.user
    comment = Comment.objects.filter(user_id=current_user.id)
    context = {
        'categories': categories,
        'settings': settings,
        'comment': comment

    }
    return render(request, 'Ecom/user_comment.html', context)



@login_required(login_url='login_user')
def comment_delete(request, id):
    current_user = request.user
    comment = Comment.objects.filter(user_id=current_user.id, id=id)
    comment.delete()
    messages.success(request, 'Your comment is successfully deleted')
    return redirect('user_comment')