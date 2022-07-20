from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from apps.product.models import Category, Product
from apps.product.permissions import CustomIsAdmin
from apps.product.serializers import CategorySerializer, ProductSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination
    # permission_classes = [IsAdminUser]
    permission_classes = [CustomIsAdmin]


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'owner']
    # sorting
    ordering_fields = ['name', 'id']
    # search
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)













    # def get_queryset(self):
    #     # переопределение  queryset это старая логика
    #     queryset = super().get_queryset()
    #
    #     filter_category = self.request.query_params.get('category')
    #     # print(filter_category) # получили то, что написано ?category =
    #     queryset=  queryset.filter(category =filter_category)
    #
    #
    #     # print(queryset)
    #     # return queryset[0:2] можно возвращать слайсы
    #     return queryset

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
