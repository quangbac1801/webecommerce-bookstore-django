# myapp/context_processors.py

from .models import Category,Cart

def menu(request):
    danh_muc = Category.objects.filter(active=True).order_by('name')
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, defaults={'session_key': request.session.session_key})
    else:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    
    cart_items = cart.items.select_related('product').all()  

    return {
        'danhmuc': danh_muc,
        'cart_items': cart_items,
    }
