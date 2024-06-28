from django.contrib import admin
from django.utils.html import mark_safe

from django import forms
from ckeditor_uploader.widgets \
import CKEditorUploadingWidget
from .models import Category, User, Products, ProductImage, Slide, Post, Order, OrderItem

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username','email','phone', 'address','is_superuser')
    list_filter = ('id', 'username')
    search_fields = ('username',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_at', 'update_at')
    search_fields = ('name',)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sale_price',)
    description = forms.CharField(widget=CKEditorUploadingWidget)
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [ProductImageInline]
    readonly_fields = ['img']
    def img(self, obj):
        if obj.images.exists():
            images = obj.images.all()
            return mark_safe(' '.join([f'<img src="/static{image.image.url}" width="100" />' for image in images]))
        return "No Image"
    

class SlideAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'img', 'active',)
    search_fields = ('title',)

    def img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="/static{obj.image.url}" width="100" />')
        return "No Image"


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'image', 'created_at', 'updated_at')
    search_fields = ('title',)
    content = forms.CharField(widget=CKEditorUploadingWidget)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('custom_order_code', 'custom_payment_method', 'custom_payment_status', 'custom_status', 'custom_total_amount', 'user_name', 'custom_created_at',)
    search_fields = ('order_code','user_name', )
    list_filter = ('payment_method', 'payment_status', 'status')
    inlines = [OrderItemInline]
    def custom_order_code(self, obj):
        return obj.order_code
    custom_order_code.short_description = "Mã đơn hàng"

    def custom_payment_method(self, obj):
        payment_method_display = {
            "cod": "Thanh toán khi nhận hàng",
            "wallet": "Thanh toán qua ví điện tử",
        }
        return payment_method_display.get(obj.payment_method, obj.payment_method)
    
    custom_payment_method.short_description = "Phương thức thanh toán"

    def custom_payment_status(self, obj):
        return obj.payment_status
    custom_payment_status.short_description = "Tình trạng thanh toán"

    def custom_status(self, obj):
        status_display = {
            "cxn": "Chờ xác nhận",
            "clh": "Chờ lấy hàng",
            "cgh": "Chờ giao hàng",
            "dg": "Đã giao",
            "dh": "Đã hủy",
        }
        return status_display.get(obj.status, obj.status)
    custom_status.short_description = "Tình trạng đơn"

    def custom_total_amount(self, obj):
        return obj.total_amount
    custom_total_amount.short_description = "Tiền thu"

    def custom_created_at(self, obj):
        return obj.created_at
    custom_created_at.short_description = "Ngày đặt"

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'User Name'


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Order, OrderAdmin)