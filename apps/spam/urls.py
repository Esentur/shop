from rest_framework.routers import DefaultRouter

from apps.spam.views import ContactView

router = DefaultRouter()
router.register('', ContactView)

urlpatterns = []
urlpatterns.extend(router.urls)
