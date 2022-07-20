from django.contrib import admin

from apps.product.models import Category, Product, Image

admin.site.register(Category)


# admin.site.register(Product)
admin.site.register(Image)


class ImangeInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImangeInAdmin]


admin.site.register(Product, ProductAdmin)

