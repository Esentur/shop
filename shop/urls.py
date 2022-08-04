"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#######for image view
from django.conf import settings
from django.conf.urls.static import static
######## general ############################
from django.contrib import admin
from django.urls import path, include
#########for swagger #######################
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

#########for swagger ######################

schema_view = get_schema_view(
    openapi.Info(
        title='Shop',
        default_version='v1',
        description='Shop project with customUser,Activation,Login,Register,Products,Categories'
                    '(filtering,ordering,searching,permissions,paginations)'
    ),
    public=True
)

################################

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('swagger/', schema_view.with_ui('swagger')),  # for documentation and provinding endpoints
                  path('api/v1/account/', include('apps.account.urls')),
                  path('api/v1/', include('apps.product.urls')),
                  path('api/v1/order/', include('apps.cart.urls')),
                  path('api/v1/spam/', include('apps.spam.urls')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # for display images
