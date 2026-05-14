# from django.shortcuts import render , get_object_or_404, redirect
# from .models import Product , Order ,OrderItem
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Product ,  Order ,OrderItem , Login


def product_list(request):
    products = Product.objects.all()
    return render (request, 'store/product_list.html',
    {'products': products})

def about_us(request):
    return render (request, 'store/about_us.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
   
    return render(request, 'store/product_detail.html', {'product': product})

def _get_cart(request):
    return request.session.get('cart',{})

def _save_cart(request , cart):
    request.session['cart'] = cart
    request.session.modified = True

def add_to_cart(request, pk):
    cart = _get_cart(request)
    pid =str(pk)
    cart[pid] = cart.get(pid,0) + 1
    _save_cart(request, cart)

    return redirect('cart')

def remove_from_cart(request , pk):
    cart = _get_cart(request)
    pid = str (pk) 
    if pid in cart:
        del cart[pid]
        _save_cart(request , cart)
    return redirect('cart') 

def cart_view(request):
    cart = _get_cart(request)
    items =[]
    total = 0
    for pid , qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        subtotal = product.price * qty 
        total+= subtotal
        items.append({
             'product': product,
             'qyt': qty ,
            'subtotal': subtotal             
         })
    return render (request ,'store/cart.html',{'items':items ,'total':total})

def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('product_list')
    
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        Mobile_no= request.POST.get("Mobile_no")
        
        order =Order.objects.create(
            full_name = full_name ,
            email = email ,
            address = address ,
            Mobile_no=Mobile_no

            )
        for pid , qyt in cart.items():
            product = get_object_or_404(Product, pk=int(pid))
            OrderItem.objects.create(order=order, product=product, quantity=qyt)
            _save_cart(request,{})
            return render(request, "store/checkout_success.html",{"order": order} )

    return render(request ,"store/checkout.html")   


def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        order = Order.objects.create(
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            Mobile_no=request.POST.get("Mobile_no")
        )

        for pid, qty in cart.items():
            product = get_object_or_404(Product, pk=int(pid))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty
            )

        _save_cart(request, {})
        return render(request, "store/checkout_success.html", {"order": order})

    return render(request, "store/checkout.html")


@csrf_exempt

def Login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            form.save()
            return redirect('l')
    else:
        form = Login()

    return render(request, 'login.html', {'form': form})


# def success_page(request):
#     return render(request, 'login.html')

