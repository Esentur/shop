from rest_framework.routers import DefaultRouter

from apps.cart.views import OrderView, CartItemView

router = DefaultRouter()
router.register('cart', CartItemView)
router.register('', OrderView)

urlpatterns = []
# urlpatterns+=router.urls
urlpatterns.extend(router.urls)
