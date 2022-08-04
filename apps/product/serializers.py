from rest_framework import serializers

from apps.product.models import Category, Product, Image, Comment, Rating
from apps.product.tasks import celery_email_about_product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ##### для отображения и скрытия parent в отображении в зависимости от наличия
        if not instance.parent:
            representation.pop('parent')
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # при создании бери email ownera
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # при создании бери email ownera
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True, read_only=True)

    # показывай комменты НО мы изменили в representation
    # comments = CommentSerializer(many=True, read_only=True)

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

        celery_email_about_product.delay(product.name)
        return product

    # покажи лайки
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.likes.filter(like=True).count())
        representation['likes'] = instance.likes.filter(like=True).count()
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rating_result = 0
        for rating in instance.ratings.all():
            print(rating.rating)
            rating_result += int(rating.rating)
        # print(instance.ratings.all().count())
        try:
            representation['rating'] = rating_result / instance.ratings.all().count()
            return representation
        except ZeroDivisionError:
            return representation

        # TODO: Отобразить рейтинг


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)
