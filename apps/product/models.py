from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.TextField(max_length=100)
    slug = models.SlugField(primary_key=True,
                            max_length=100,
                            unique=True,
                            blank=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children')

    def save(self, *args, **kwargs):
        self.slug = self.title.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.slug}'
        else:
            return self.slug


class Product(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='products')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')

    # сейчас у 1 продукта 1 картина
    # image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Like(models.Model):
    '''
    Модель лайков
    '''
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='likes',
                              verbose_name='Владелец лайка')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='likes',
                                verbose_name='Товар')
    like = models.BooleanField('Лайк', default=False)

    def __str__(self):
        return f'{self.product} {self.like}'


class Rating(models.Model):
    '''
    Модель  рейтинга
    '''
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='ratings',
                              verbose_name='Владелец рейтинга')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='ratings',
                                verbose_name='Продукт')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ], default=1
    )

    def __str__(self):
        return f'{self.product} - {self.rating}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment"
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

