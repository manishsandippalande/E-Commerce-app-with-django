from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from merchapp.models import products, cart, userextrainfo, orders, wishlist, history, RegistrationData, ContactPage
from django.contrib.auth import authenticate , login , logout
import os
import random
from django.core.mail import send_mail
# Create your views here.


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        fname = request.POST['fname']
        uemail = request.POST['email']
        opass = request.POST['pass']  #opass means original pass it is used because pass is builtin keyword
        cpass = request.POST['cpass']
        otp = str(random.randint(100000, 999999))
        msg = f"Hello {fname},\n Your OTP For OnlyX Registration is {otp}"
        send_mail(
            "OnlyX OTP Verification",
            msg,
            "manishpalande55@gmail.com",
            [uemail],
            fail_silently=False,
        )
        context = {}
        if fname == '' or uemail == '' or opass == '' or cpass == '':
            context['errormessage'] = 'Please Enter All Your Feilds'
            return render(request, 'register.html',context)
        else:
            if opass == cpass:
                # userdata = User.objects.create(first_name=fname, username=email, email = email)
                # userdata.set_password(opass)
                # userdata.save()
                registration_data = RegistrationData.objects.create(fname=fname,email=uemail,password=opass,otp=otp)
                registration_data.save()
                context['registration_data_email'] = registration_data.email
                # Redirect to OTP verification page
                return render(request, 'otp_verification.html', context)
            else:
                context['errormessage'] = 'Passwords are not matching'
                return render(request, 'register.html', context)


def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        uemail = request.POST['registration_data_email']
        registration_data = RegistrationData.objects.get(email=uemail)
        
        if entered_otp == registration_data.otp:
            # OTP is valid, transfer data to User model
            user = User.objects.create(
                first_name=registration_data.fname,
                username=registration_data.email,
                email=registration_data.email
            )
            user.set_password(registration_data.password)
            user.save()

            registration_data.delete()

            # Optionally, you can log in the user here
            # ...

            context = {'successmessage': 'Registered Successfully.'}
            return render(request, 'login.html', context)
        else:
            context['error'] = "Otp Is Invalid"
            return render(request, 'otp_verification.html', context)
        # registration_data.delete()
        

    return render(request, 'otp_verification.html')

def userlogin(request):
    if request.method=='GET':
        return render(request, 'login.html')
    else:
        context = {}
        useremail = request.POST['email']
        userpass = request.POST['pass']
        if useremail == '' or userpass == '':
            context['errormsg'] = '*Please Fill Both Fields.'
            return render(request, 'login.html', context)
        else:
            u = authenticate(username = useremail, password = userpass)
            if u is not None:
                login(request, u) 
                print(request.user.is_authenticated)
                print(u)
                return redirect('/extrainfo')
            else:
                context['errormsg'] = '*Wrong Credentials'
                return render(request, 'login.html', context)
            


def home(request):
    userid = request.user.id
    print(f"email id is : {userid}")
    data = products.objects.all()[:5]
    discountdata = products.objects.all().order_by('-discount')[:5]
    category = products.objects.values('category').distinct()
    context = {}
    context['trending_data'] = data
    context['discount_data'] = discountdata
    context['categories']=category
    return render(request, 'home.html', context)

def productspage(request,cat):
    context = {}
    if cat == 'all':
        data = products.objects.all()
        context['all_data'] = data
        return render(request, 'products.html', context)
    else:
        data = products.objects.filter(category=cat)
        context['all_data'] = data
        return render(request, 'products.html', context)
    



def productdetails(request, pid):
    context ={}
    proddetail = products.objects.filter(id=pid)
    context['productdetail']= proddetail[0]
    return render(request, 'details.html', context)

from django.contrib import messages
def addtocart(request, productid):
    userid = request.user.id
    if userid:
        product = products.objects.filter(id=productid)
        cur_user = User.objects.filter(id=userid)
        cartprod = cart.objects.create(pid = product[0], uid = cur_user[0])
        cartprod.save()
        messages.success(request, "Your product is added to cart")
        return redirect(f'/productdetails/{productid}')
    else:
        return redirect('/login')


def cartPage(request):
    userid = request.user.id
    if userid:
        context ={}
        cartprods = cart.objects.filter(uid = userid)
        totalprods = cartprods.count()
        totalamount = 0
        for i in cartprods:
            totalamount += i.pid.disprice * i.quantity
        context['cartprods'] = cartprods
        context['totalprods']=totalprods
        context['totalamount']=totalamount
        return render(request, 'cart.html', context)
    else:
        return redirect('/login')

def delcartitem(request, cid):
    cartitem = cart.objects.filter(id = cid)
    cartitem[0].delete()
    return redirect('/cart')

def cartquantity(request, cartid, incr):
    cartproduct = cart.objects.filter(id=cartid)
    if incr == '0':
        newQuant = cartproduct[0].quantity - 1
    else :
        newQuant = cartproduct[0].quantity + 1
    cartproduct.update(quantity = newQuant)
    return redirect("/cart")

def extrainfo(request):
    userid = request.user.id
    user = User.objects.filter(id = userid)
    Userinfo = userextrainfo.objects.filter(uid = userid)
    if userid:
        if Userinfo:
            return redirect('/')
        else:
            if request.method == 'GET':
                return render(request, 'extrainfoo.html')
            else:
                user = User.objects.get(id = userid)
                Address = request.POST['Address']
                Phone = request.POST['Phone']
                profilepic = request.FILES['profilepic']
                userinfo = userextrainfo.objects.create(uid =user,address=Address,phonenum=Phone, profilepic= profilepic)
                userinfo.save()
                return redirect('/')
    else:
        return redirect('/login')
        

    
    

def userlogout(request):
    logout(request)
    return redirect('/')

def accountPage(request):
    userid = request.user.id
    print('user= ',userid)
    if userid :
        context = {}
        accountInfo = User.objects.filter(id = userid)
        extrainfo = userextrainfo.objects.filter(uid=userid)
        context['accountinfo']=accountInfo[0]
        print(extrainfo)
        context['extrainfo'] = extrainfo[0]
        return render(request, 'account.html', context)
    else:
        return redirect('/login')
    

# sorting products by price

def sort(request, incr):
    context = {}
    if incr=='0':
        col='price'
    else:
        col='-price'
    allemp = products.objects.all().order_by(col)
    context['all_data']=allemp
    return render(request, 'products.html', context)

def placeorder(request):
    userid = request.user.id
    orderid = random.randrange(1000,9999)
    # fetching the logedin user's cart
    cartprods = cart.objects.filter(uid = userid)
    # calculating the total payable amount and quantity
    count = len(cartprods) #quantity
    billamount = 0 
    for i in cartprods:
        billamount += i.pid.disprice * i.quantity
    context ={}
    context['count'] = count
    context['billamount'] = billamount
    # here we are adding each cart product to our orders table 
    for prod in cartprods:
        order = orders.objects.create(orderid=orderid ,uid =prod.uid, pid=prod.pid , quantity= prod.quantity)
        order.save()
    # here we are deleting cart prods from cart after placing order
    cartprods.delete()

    orders_prods = orders.objects.filter(uid = userid)
    context['allprods'] = orders_prods
    return render(request, 'placeorder.html', context)


import razorpay
def makepayment(request): 
    # fetch orders table
    userid = request.user.id
    orderdetails = orders.objects.filter(uid = userid)
    #  calculate the total amount
    bill = 0
    for ord in orderdetails:
        bill += ord.pid.disprice * ord.quantity
        ordid = ord.orderid

    client = razorpay.Client(auth=("rzp_test_IeYvvSO8OOroz1", "yCacb9dOv7My28Z3OWLRHZO9"))
    data = { "amount": bill*100, "currency": "INR", "receipt": str(ordid) }
    payment = client.order.create(data=data)
    context ={}
    context['paydata']=payment
    if payment:
        for i in orderdetails:
            historydata = history.objects.create(orderid=i.orderid, uid =i.uid, pid=i.pid , quantity= i.quantity)
            historydata.save() #here we need to add buyed products in history table and remove it from orders table
        else:
            ord = orders.objects.all()
            ord.delete()
    print(payment)
    return render(request, 'payment.html', context)

def addtowishlist(request, productid):
    userid = request.user.id
    if userid:
        product = products.objects.filter(id=productid)
        cur_user = User.objects.filter(id=userid)
        cartprod = wishlist.objects.create(pid = product[0], uid = cur_user[0])
        cartprod.save()
        return redirect(f'/productdetails/{productid}')
    else:
        return redirect('/login')
    
def wishlistpage(request):
    userid = request.user.id
    if userid:
        context = {}
        wishlistprods = wishlist.objects.filter(uid = userid)
        context['wishlistprods'] = wishlistprods
        return render(request, 'wishlist.html',context)
    else:
        redirect('/login')

def transfercart(request, pid):
    userid = request.user.id
    if userid:
        product = products.objects.filter(id=pid)
        cur_user = User.objects.filter(id=userid)
        cartprod = cart.objects.create(pid = product[0], uid = cur_user[0])
        cartprod.save()
        wishlist_product = wishlist.objects.filter(pid = pid)
        wishlist_product[0].delete()
        return redirect(f'/wishlist')
    else:
        return redirect('/login')
    

def historypage(request):
    context ={}
    userid = request.user.id
    user_history = history.objects.filter(uid = userid)
    context['historypage'] = user_history
    return render(request, 'history.html', context)


def sendemailto(request):
    userid = request.user.username
    msg = f"Congratulations Your Order is Successfully Placed and will be delivered soon..."
    send_mail(
        "OnlyX Order Is Placed Successfully",
        msg,
        "manishpalande55@gmail.com",
        [userid],
        fail_silently=False,
    )
    return redirect('/')



def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    userid = request.user.id
    if request.method == 'GET':
        return render(request, 'contact.html')
    else:
        cur_user=User.objects.filter(id=userid)
        msg = request.POST['msg']
        data = ContactPage.objects.create(uid=cur_user[0],messege=msg)
        data.save()
        return render(request, 'contact.html')