from django.urls import include, path
from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),
    path('user-info/', views.user_info, name="user_info"),
    path('user-infor/edit/', views.edit_user, name='edit_user'),

    path('news/', views.blog, name='news'),

    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('product_detail/<int:product_id>', views.product_detail, name="product_detail"),

    path('addcart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:product_id>/', views.update_cart, name='update_cart'),

    path('checkout/', views.checkout_view, name='checkout'),
    path('process_order/', views.process_order, name='process_order'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),

     path('statistics/', views.statistics_view, name='statistics'),
]
