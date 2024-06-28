from rest_framework.serializers import ModelSerializer
from myapp.models import *

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ImageProductSeralizer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]

class ProductSerializer(ModelSerializer):
    category = CategorySerializer()
    images = ImageProductSeralizer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ["id", "name", "sale_price", "create_at", "update_at", "images", "category"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'phone', 'address', 'avatar']
        extra_kwargs={
            'password':{'write_only':'true'}
        }
    def create(self, vailidated_data):
        user=User(**vailidated_data)
        user.set_password(vailidated_data['password'])
        user.save()
        return user
    
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"