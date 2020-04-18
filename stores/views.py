from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from stores.models import *
import json
from datetime import datetime

def home(request):

    return render(request,"home.html")

def vendor_signup(request):
    if request.method == "POST":
        fullname=request.POST["fullname"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        first_name=fullname.split()[0]
        last_name=" ".join(fullname.split()[1:])
        user= User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username, 
            password=password, 
            email=email
        )
        login(request, user)
        profile=Profile.objects.create(
            user=user,
            user_type='VR'
        )
        vendor_profile =Vendor_profile.objects.create(user=user)
        return redirect("/dashboard/")
        
    return render(request,"vendor_signup.html")
    

def vendor_signin(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(username=username, password=password)

		if user != None:
			login(request, user)
			return redirect("/dashboard/")

	return render(request, "vendor_signin.html")

def signout(request):
	logout(request)
	return redirect("/")

def mystores(request):
    stores=Store.objects.filter(owner=request.user)
    return render(request,"stores_dash.html",{"stores":stores})

def dashboard(request):
    stores=Store.objects.filter(owner=request.user)
    orders=Order.objects.filter(store__in=stores)
    labels=[]
    data=[]
    for order in orders:
        total=0
        date=str(order.timestamp.date())

        for item in order.order_items.all():
            amt=item.product.price * item.quantity
            total+=amt
        if date not in labels:
            labels.append(date)
            data.append(total)
        else:
            index=labels.index(date)
            data[index]+=total
    print(data, labels)

    return render(request,"dashboard.html",{"labels":json.dumps(labels), "data":data})

def myorders(request):
    stores=Store.objects.filter(owner=request.user)
    orders=Order.objects.filter(store__in=stores)
    return render(request,"myorders.html",{"orders":orders})

def mycustomers(request):
    stores=Store.objects.filter(owner=request.user)
    orders=Order.objects.filter(store__in=stores)
    customers=[]
    for order in orders:
        if order.customer not in customers:
            customers.append(order.customer)
    return render(request,"mycustomers.html", {"customers":customers})

def create_store(request):
    if request.method=="POST" and request.user.is_authenticated:
        name=request.POST["name"]
        
        title=request.POST["title"]
        subtitle=request.POST["subtitle"]
        user=request.user
        slug="-".join(name.lower().split())
        store=Store.objects.create(
            name=name,
            
            owner=user,
            slug=slug,
            title=title,
            subtitle=subtitle
        )
        return redirect("/dashboard/")

def edit_store(request, pk):
    store=Store.objects.get(pk=pk)
    products=Product.objects.filter(store=store, manufacturer=request.user)
    return render(request, "edit_store.html",{"store":store, "products":products})

def add_product(request, store_id):
    store=Store.objects.get(pk=store_id)
    if request.method=="POST" and store.owner == request.user:
        product_name=request.POST["product_name"]
        manufacturer=request.POST["manufacturer"]
        price=request.POST["price"]
        stock=request.POST["stock"]
        description=request.POST["description"]

        product=Product.objects.create(
            store=store,
            product_name=product_name,
            manufacturer=manufacturer,
            price=price,
            stock=stock,
            description=description,
            sales_count=0,
            rating=2.5
        )
        return redirect(f"/edit/store/{store_id}")

def edit_product(request, pk):
    product=Product.objects.get(pk=pk)            
    if request.method=="POST" and product.store.owner == request.user:
        product_name=request.POST["product_name"]
        manufacturer=request.POST["manufacturer"]
        price=request.POST["price"]
        stock=request.POST["stock"]
        description=request.POST["description"]

        product.product_name=product_name
        product.manufacturer=manufacturer
        product.price=price
        product.stock=stock
        product.description=description
        product.save()

        return redirect(f"/edit/store/{product.store.id}")

def store_page(request, store_slug):
    store=Store.objects.get(slug=store_slug)
    ssid=request.session.session_key
    if not Cart.objects.filter(ssid=ssid, store=store).exists():
        Cart.objects.create(
            ssid=ssid,
            store=store
        )
    products=Product.objects.filter(store=store)
    return render(request, "store_page.html",{"products":products, "store":store})
    
def add_to_cart(request, product_id):
    product=Product.objects.get(id=product_id)
    store=product.store
  
    ssid=request.session.session_key
    if Cart.objects.filter(ssid=ssid, store=store).exists():
        cart= Cart.objects.get(ssid=ssid, store=store)
        if CartItem.objects.filter(cart=cart,product=product).exists():
            cartitem =CartItem.objects.get(cart=cart,product=product)
            cartitem.quantity += 1
            cartitem.save()
        else:
            cartitem=CartItem.objects.create(cart=cart,product=product)
    return redirect(f"/store/{product.store.slug}/")

def  cart_page(request, store_slug):
    store=Store.objects.get(slug=store_slug)
    ssid=request.session.session_key
    if not Cart.objects.filter(ssid=ssid, store=store).exists():
        cart= Cart.objects.create(
            ssid=ssid,
            store=store
        )
    else:
        cart= Cart.objects.get(ssid=ssid, store=store)

    cartitems= CartItem.objects.filter(cart=cart)
    total=0

    for item in cartitems:
        cost=item.product.price * item.quantity
        total+=cost

    return render(request, "cart_page.html", {"cartitems":cartitems,"cart":cart, "total":total})


def remove_item(request, cart_item_id):
    cart_item=CartItem.objects.get(id=cart_item_id)
    store=cart_item.cart.store
    cart_item.delete()
    return redirect(f"/store/{store.slug}/cart/")


def checkout(request, cart_id):
    cart=Cart.objects.get(pk=cart_id)
    cart_items=CartItem.objects.filter(cart=cart)

    name=request.POST["name"]
    address=request.POST["address"]
    phone=request.POST["phone"]
    email=request.POST["email"]

    customer=Customer.objects.filter(email=email).exists()

    if not customer:
        customer=Customer.objects.create(
            name=name,
            email=email,
            address=address,
            phone=phone
        )
    else:
        customer=Customer.objects.get(email=email)

    order=Order.objects.create(customer=customer, store=cart.store)

    for item in cart_items:
        order_items=OrderItem.objects.create(
            order=order, 
            product=item.product,
            quantity=item.quantity
        )

    order_items=OrderItem.objects.filter(order=order)

    total=0

    for item in order_items:
        cost=item.product.price * item.quantity
        total+=cost 

    order_id=str(order.id)
    pad= 6- len(order_id)

    order_id= pad*"0" + order_id

    return render(request, "order_confirmation.html",{"order": order,
                                                    "cart":cart, 
                                                    "items":order_items,
                                                    "order_id":order_id,
                                                    "total":total,
                                                    "customer":customer})

  