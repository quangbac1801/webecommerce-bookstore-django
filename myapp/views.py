from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from .models import *
from django.contrib.auth import login,logout ,authenticate
from django.contrib import messages
from .forms import CreateUserForm,LoginForm, UpdateUserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Sum
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    slides = Slide.objects.filter(active=True)
    sort_by = request.GET.get('sort_by')
    
    # Thực hiện sắp xếp trước khi chia nhỏ tập dữ liệu
    if sort_by == 'price_asc':
        product_list = Products.objects.all().order_by('sale_price')
    elif sort_by == 'price_desc':
        product_list = Products.objects.all().order_by('-sale_price')
    elif sort_by == 'newest':
        product_list = Products.objects.all().order_by('-create_at')
    elif sort_by == 'oldest':
        product_list = Products.objects.all().order_by('create_at')
    elif sort_by == 'best_selling':
        product_list = Products.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')
    else:
        product_list = Products.objects.all().order_by('-create_at')

    paginator = Paginator(product_list, 16)  
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.page(int(page_number))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    query = request.GET.get('tk')
    if query and query.strip() != '':
        products = Products.objects.filter(name__icontains=query).order_by('-create_at')
    else:
        products = page.object_list

    context = {
        'slides': slides,
        'products': products,
        'page': page,  
        'sort_by': sort_by,
    }
    return render(request, "myapp/index.html", context)

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Đăng ký thành công! Chào mừng bạn đến với trang web của chúng tôi.')
            return redirect('home')
    else: 
        form = CreateUserForm()
    return render(request, "myapp/register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  
                return redirect('home')
            else:
                messages.error(request, "Tài khoản hoặc mật khẩu không chính xác.")
    else:
        form = LoginForm()
    return render(request, "myapp/login.html", {'form': form})

def logout_user(request):
    logout(request)
    return redirect("home")

def blog(request):
    posts = Post.objects.filter(active=True).order_by('-created_at')  
    return render(request, 'myapp/blog.html', {'posts': posts})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Products.objects.filter(category=category)
    categories = Category.objects.filter(active=True).order_by('name')
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'myapp/category_products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    similar_products = Products.objects.filter(category=product.category).exclude(id=product_id)[:3]
    categories = Category.objects.filter(active=True).order_by('name')
    return render(request, "myapp/product_detail.html", {"product": product, "similar_products":similar_products,'categories': categories })

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, defaults={'session_key': request.session.session_key})
    else:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = get_cart(request)
    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity = F('quantity') + quantity
    cart_item.save()
    messages.success(request, 'Thêm vào giỏ hàng thành công')
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'cart_detail'))
    return redirect(next_url)


def cart_detail(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()
    total_price = cart.total_price
    return render(request, 'myapp/carts.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return redirect('cart_detail')


@require_POST
def update_cart(request, product_id):
    cart = get_cart(request)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        if 'add' in request.POST:
            cart_item.quantity = F('quantity') + 1
        elif 'subtract' in request.POST and cart_item.quantity > 1:
            cart_item.quantity = F('quantity') - 1
        cart_item.save()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart_detail')


@login_required
def checkout_view(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()
    total_price = cart.total_price

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'myapp/checkout.html', context)

def process_order(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()
    total_price = cart.total_price
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if not cart_items:
            messages.error(request, 'Giỏ hàng của bạn đang trống.')
            return redirect('cart_detail')

        order = Order.objects.create(
            user=request.user,
            total_amount=total_price,
            payment_method=payment_method,
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.sale_price,
            )

        cart.items.all().delete()

        send_order_email(order)

        if payment_method == 'cod':
            messages.success(request, 'Đặt hàng thành công! Đơn hàng của bạn đang được xử lý.')
            return redirect('home')
        elif payment_method == 'wallet':
            return redirect(reverse('payment:payment', kwargs={'order_code': order.order_code}))

    return redirect('cart_detail')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'cxn':
        order.status = 'dh'
        order.save()
        messages.success(request, "Đơn hàng đã được hủy")
    return redirect("user_info")


def send_order_email(order):
    subject = 'Xác nhận đơn hàng'
    template = 'myapp/contentmail.html'

    context = {
        'order': order,
        'domain': 'bookstore.com',
    }

    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)  

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,  
        [order.user.email],  
        html_message=html_message,  
    )


@login_required
def user_info(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    context ={
        'user':user,
        'orders':orders,
    }
    return render(request, 'myapp/user_info.html', context)

@login_required
def edit_user(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin thành công")
            return redirect("user_info")
    else:
        form = UpdateUserForm(instance=request.user)
    
    return render(request, 'myapp/update_userinfo.html', {'form': form})


def get_monthly_stats():
    current_year = timezone.now().year
    monthly_revenues = []

    for month in range(1, 13):
        revenue_for_month = Order.objects.filter(
            created_at__year=current_year,
            created_at__month=month
        ).aggregate(total_amount=Sum('total_amount'))['total_amount'] or Decimal('0.0')
        
        monthly_revenues.append(float(revenue_for_month))  
    return monthly_revenues


def statistics_view(request):
    monthly_revenues = get_monthly_stats()
    total_users = User.objects.count()
    current_month = timezone.now().month
    current_year = timezone.now().year
    orders_this_month = Order.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).count()
    total_orders_this_month = Order.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total_amount=Sum('total_amount'))['total_amount'] or Decimal('0.0')
    context = {
        'monthly_revenues': monthly_revenues,
        'total_users': total_users,
        'orders_this_month': orders_this_month,
        'total_orders_this_month':total_orders_this_month,
    }
    return render(request, 'admin/statistics.html', context)
