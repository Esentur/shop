from rest_framework.routers import DefaultRouter

from apps.cart.views import OrderView

router = DefaultRouter()
router.register('', OrderView)

urlpatterns = []
# urlpatterns+=router.urls
urlpatterns.extend(router.urls)
