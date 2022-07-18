from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.product.views import CategoryView

router = DefaultRouter()
router.register('category', CategoryView)
urlpatterns = [
    # path('category/', CategoryView.as_view({'get': 'list'})),
    path('', include(router.urls)),
]
