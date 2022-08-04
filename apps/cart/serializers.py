from rest_framework import serializers

from apps.account.sent_mail import send_order_confirmation
from apps.account.tasks import celery_send_order_confirmation
from apps.cart.models import Order, CartItem, Cart


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['customer']
        cart = user.carts.first()
        validated_data['total_cost'] = cart.total_cost
        validated_data['info'] = ''
        for _ in cart.cart_items.all():
            validated_data['info'] += f'{_.product} {_.total_cost} {_.quantity} \n'
        # send_order_confirmation(user.email, validated_data['info'])
        celery_send_order_confirmation.delay(user.email, validated_data['info'])
        cart.cart_items.all().delete()
        return super().create(validated_data)


# todo Отправить пиьсмо на почту покупателю

# def create(self, validated_data):
#     quantity_order = validated_data['quantity']
#     product = validated_data['product']
#     quantity_product = product.amount
#
#     if quantity_order > quantity_product:
#         raise serializers.ValidationError(
#             f'Вы запросили {quantity_order} продукта : {product}, остаток {quantity_product}. Сорян так что')
#     product.amount -= quantity_order
#     product.save()
#     return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        # fields = '__all__'
        exclude = ['cart']

    def create(self, validated_data):
        user = self.context.get('request').user
        print(user)
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item = CartItem.objects.create(
            cart=cart,
            product=validated_data['product'],
            quantity=validated_data['quantity']
        )
        quantity_order = validated_data['quantity']
        product = validated_data['product']
        quantity_product = product.amount

        if quantity_order > quantity_product:
            raise serializers.ValidationError(
                f'Вы запросили {quantity_order} продукта : {product}, остаток {quantity_product}. Сорян так что')
        product.amount -= quantity_order
        product.save()
        return cart_item
