from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from apps.product.models import Category, Product, Comment, Like, Rating
from apps.product.permissions import CustomIsAdmin
from apps.product.serializers import CategorySerializer, ProductSerializer, CommentSerializer, RatingSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [CustomIsAdmin]


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filters
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'owner']
    ordering_fields = ['name', 'id']
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        try:
            like_object, _ = Like.objects.get_or_create(owner=request.user, product_id=pk)
            like_object.like = not like_object.like
            like_object.save()
        except:
            return Response('Нет такого продукта! ')
        status = 'liked'
        if like_object.like:
            return Response({'status': status})
        status = 'unliked'
        return Response({'status': status})

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(owner=request.user, product_id=pk)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status='201')

    def get_permissions(self):
        # print(self.action)
        if self.action in ['list', 'retrieve']:
            permissions = [IsAuthenticated]
        elif self.action == 'like' or self.action=='rating':
            permissions = [IsAuthenticated]
        else:
            permissions =[IsAuthenticated]
        return [p() for p in permissions]


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)  # выдаем юзера как овнер коммента
        return Response(serializer.data, status=status.HTTP_201_CREATED)
