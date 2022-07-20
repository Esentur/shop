from rest_framework import serializers

from apps.product.models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ## print(representation)
        ## representation['hello']='hello John'
        ##### для отображения и скрытия parent в отображении в зависимости от наличия
        if not instance.parent:
            representation.pop('parent')
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # при создании бери email ownera
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        # print(requests)
        images = requests.FILES
        product = Product.objects.create(**validated_data)

        for image in images.getlist('images'):
            Image.objects.create(product=product, image=image)
        return product
