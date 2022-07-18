from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from apps.product.models import Category
from apps.product.serializers import CategorySerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#
# class CategoryView(ViewSet):
#     def list(self, request):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request): # не POST потому что тут ViewSet
#         serializer = CategorySerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
