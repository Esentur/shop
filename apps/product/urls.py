from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.product.views import CategoryView, ProductView, CommentView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('product', ProductView)
router.register('comment', CommentView)

urlpatterns = [
    # path('category/', CategoryView.as_view({'get': 'list'})),
    path('', include(router.urls)),
]
