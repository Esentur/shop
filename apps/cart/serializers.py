from rest_framework import serializers

from apps.cart.models import Order


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        quantity_order = validated_data['quantity']
        product = validated_data['product']
        quantity_product = product.amount

        if quantity_order > quantity_product:
            raise serializers.ValidationError(
                f'Вы запросили {quantity_order} продукта : {product}, остаток {quantity_product}. Сорян так что')
        product.amount -= quantity_order
        product.save()
        return super().create(validated_data)
