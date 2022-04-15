from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from requests import post
from .form import AddressForm, UserCreateForm,PassChangeForm,PassChangeForm,UserProfileChangeForm,AddressForm,ContactForm
# from django.contrib import messages
from .models import ProductModel  #import
from .models import ProductModel,MainCategoryModel,SubCategoryModel,Cart,Address,Myorder,Contact
from django.conf import settings 
from django.core.mail import send_mail
from django.contrib import messages



# key id - rzp_test_uqhoYnBzHjbvGF
# key secret - jEhBs6Qp9hMeGfq5FyU45cVi

# Create your views here.
from .form import UserCreateForm

import razorpay



def logoutUser(request):
    logout(request)
    return redirect('login')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')

    return render(request, 'login.html')

def registration(request):
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'😃 Registration Successfully Done')
            return redirect("/login")
    con = {'form':form}
    return render(request,"registration.html",con)

def ChangePassView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PassChangeForm(user = request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Password Successfully Changed') 
                return redirect('/login/')

        else:
            form = PassChangeForm(user =request.user)
            
        context= {'form':form,}
        return render(request,'changepassword.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/login/')

# User Profile Update
def ProfileView(request):
    if request.user.is_authenticated:
        form =UserProfileChangeForm(instance=request.user)
        context = {'form':form}
        if request.method == 'POST':
            form =UserProfileChangeForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                messages.info(request,'Profile Successfully Updated')
                return redirect('/profile/')
            else:
                form =UserProfileChangeForm(instance=request.user)
                user_data = request.user
                context = {'form':form,'user_data':user_data}
                return render(request,'updateprofile.html',context)
        
        return render(request,'updateprofile.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/login/')

def index(request):
    all = ProductModel.objects.all()[:5]
    cat = SubCategoryModel.objects.all()
    list1 = []
    sub_total = 0
    shipping_total = 0
    
    if request.user.is_authenticated:
        prod = Cart.objects.filter(user=request.user)
        count = Cart.objects.filter(user=request.user).count()
        for x in prod:
            z = x.product.sell_price * x.quantity
            list1.append(z)
            sub_total = sum(list1)
            shipping_total = sub_total + 70
    else:
        prod = "hello"
        count = 0

    

    con = {'all':all,'prod':prod,'sub_total':sub_total,'shipping_total':shipping_total,'cat':cat,"count":count}
    return render(request,"index.html",con)

def bloggrid(request):
    return render(request,"bloggrid.html")

def blog(request):
    return render(request,"blog.html")    

def cart(request):
    cat = SubCategoryModel.objects.all()

    if request.user.is_authenticated:
        prod = Cart.objects.filter(user=request.user)
        count = Cart.objects.filter(user=request.user).count()

        list1 = []
        sub_total = 0
        shipping_total = 0
        for x in prod:
            z = x.product.sell_price * x.quantity
            list1.append(z)
            sub_total = sum(list1)
            shipping_total = sub_total + 70
        con = {'prod':prod,'sub_total':sub_total,'shipping_total':shipping_total,'cat':cat,"count":count}
        return render(request,"cart.html",con)
    else:
        return redirect("login")

def single(request):
    return render(request,"single.html")

def category(request):
    cat = SubCategoryModel.objects.all
    cid=request.GET.get("cid")
    mid = request.GET.get("mid")
    mcate = MainCategoryModel.objects.all()
    count = Cart.objects.filter(user=request.user).count()
    prod = Cart.objects.filter(user=request.user).order_by('id')

    list1=[]
    sub_total=1
    shipping_total = 1
    for x in prod:
        z=x.product.sell_price * x.quantity
        list1.append(z)
        sub_total = sum(list1)
        shipping_total = sub_total + 70

    if cid:
        all_prod = ProductModel.objects.filter(scate_id=cid)
    elif mid:
        all_prod = ProductModel.objects.filter(mcate_id=mid)    
    else:
        all_prod=ProductModel.objects.all()    
    con = {'all_prod':all_prod,'cat':cat,'prod':prod,'sub_total':sub_total,'shipping_total':shipping_total,'count':count,'mcate':mcate}

    return render(request,"category.html",con)

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user
            x.save()
            messages.success(request,'😃 Contact Successfully Submitted')
            return redirect("contact")
        else:
            return redirect("contact")   
    else:
        pass
    con = {'form':form}         
    return render(request,"contact.html",con)



def wishlist(request):
    return render(request,"wishlist.html")
       
def dashboard(request):
    return render(request,"dashboard.html")

def pcbox(request):   
    return render(request,"pcbox.html")

def product(request,id):
    single = ProductModel.objects.get(id=id)
    con ={'single':single}
    
    return render(request,"product.html",con)

def Add_to_cart(request,id):
    if request.user.is_authenticated:
        user = request.user
        get_id = Cart.objects.filter(product__id = id).exists()
        if get_id:
            cart = Cart.objects.get(product__id = id)
            if cart: 
                cart.quantity += 1
                cart.save()
            return redirect("cart")
        else:        
            prod = ProductModel.objects.get(id = id)
            Cart(user=user,product=prod).save()
            return redirect("cart")
    else:
        return redirect("login")

def cart_remove(request,id):
    
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect("cart")

def cart_plus(request,id):
    cart = Cart.objects.get(id=id)
    if cart:
        cart.quantity += 1
        cart.save()
        return redirect("cart")
    else:
        return redirect("cart")

def cart_minus(request,id):
    cart = Cart.objects.get(id=id)
    if cart:
        if(cart.quantity == 1): Cart.objects.get(id=id).delete()
        else:
            cart.quantity -= 1
            cart.save()
        return redirect("cart")
    else:
        return redirect("cart")
    
def address(request):
    cat = SubCategoryModel.objects.all()
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user
            x.save()
            return redirect("checkout")
        else:
            return redirect("address")
    else:
        pass
    con = {'form':form,'cat':cat}
    return render(request,"address.html",con)            

def categorybox(request,id):
    single_prod = ProductModel.objects.get(id=id)
    con={'single_prod':single_prod}

    return render(request,"categorybox.html")

def comingsoon(request):
    return render(request,"comingsoon.html")

def about(request):
    return render(request,"about.html") 

def categorymarket(request):
    return render(request,"categorymarket.html")
    
def checkout(request):
    cat = SubCategoryModel.objects.all()
    cart = Cart.objects.all().count()
    prod = Cart.objects.filter(user=request.user).order_by('id')
    count = Cart.objects.filter(user=request.user).count()
    all_address =   Address.objects.filter(user=request.user)
    add_id=request.GET.get("add")
    list1=[]
    sub_total=1
    shipping_total = 1
    for x in prod:
        z=x.product.sell_price * x.quantity
        list1.append(z)
        sub_total = sum(list1)
        shipping_total = sub_total + 70
        if add_id:
            add = Address.objects.get(id=add_id)
            prod1 = x.product
            qty = x.quantity
            Myorder(user = request.user,address=add,product=prod1,quantity=qty).save()
            x.delete()
            # if cart == 0:
            #     return redirect('order')

    

    amount = shipping_total*100 #100 here means 1 dollar,1 rupree if currency INR
    client = razorpay.Client(auth=('rzp_test_uqhoYnBzHjbvGF','jEhBs6Qp9hMeGfq5FyU45cVi'))
    response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
    print(response,"****************************************")
    if add_id:
        user = request.user
        subject = 'welcome to Mobile Shop'
        message = f'Hi {user}, Thank you for Shopping.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('order')

    con = {'all_address':all_address,'prod':prod,'sub_total':sub_total,'shipping_total':shipping_total,'response':response,'cat':cat,'count':count}
    return render(request,"checkout.html",con)

def searchview(request):
    srch = request.GET.get("srch")
    if srch:
        prod = ProductModel.objects.filter(name__contains=srch)

    con = {'all_prod':prod}
    return render(request,"category.html",con)

def order(request):
    cat = SubCategoryModel.objects.all()
    if request.user.is_authenticated:
        ord = Myorder.objects.filter(user=request.user)
        list1 = []
        sub_total = 1
        shipping_total = 1
        status = "pending"
        for x in ord:
            z = x.product.sell_price * x.quantity
            list1.append(z)
            sub_total = sum(list1)
            shipping_total = sub_total + 70
            
            if status == "confirm order":
                messages.success(request,'😃 Contact Successfully Submitted')

        con = {'ord':ord,'sub_total':sub_total,'shipping_total':shipping_total,'cat':cat}
        return render(request,"order.html",con)
    else:
        return redirect("login")    
