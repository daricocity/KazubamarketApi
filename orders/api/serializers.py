from products.models import Product
from orders.models import Order, Cart
from rest_framework import serializers

########## ORDER LIST SERIALIZER ##########
class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'order', 'product', 'quantity', 'line_total']

########## ORDER LIST SERIALIZER ##########
class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

########## ORDER SERIALIZER ##########
class CartSerializer(serializers.ModelSerializer):

	class Meta:
		model = Cart
		fields = ['user', 'order', 'product', 'quantity', 'line_total']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    cart = CartSerializer(source = 'cart_set', many = True, read_only = True)

    class Meta:
        model = Order
        fields = ['user', 'order_id', 'cart', 'total']

    def get_user(self, obj):
        return obj.request.user

    def create(self, validated_data):
    	carts_data = self.context['request'].data
    	oder_total = carts_data['total']
    	cart_item = carts_data['cartItems']
    	order = Order.objects.create(user = self.context['request'].user, total = oder_total)
    	for i in cart_item:
    		Cart.objects.create(
    			user = self.context['request'].user, 
    			order = order, product = Product.objects.get(pk = int(i['id'])), 
    			quantity = i['quantity'], 
    			line_total = float(i['regular_price'])*float(i['quantity'])
    		)
    	return order