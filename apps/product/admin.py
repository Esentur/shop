from django.contrib import admin

from apps.product.models import Category, Product, Image, Comment, Like, Rating

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Comment)


class ImangeInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 5
    extra = 0


class CommentInAdmin(admin.TabularInline):
    model = Comment
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImangeInAdmin, CommentInAdmin]
    list_display = ['id', 'name', 'price', 'count_like']

    def count_like(self, obj):
        return obj.likes.filter(like=True).count()


admin.site.register(Product, ProductAdmin)
