from rest_framework import viewsets, generics

from product_shop.products.models import Product, Category, SubCategory
from product_shop.products.serializers import ProductSerializer, CategorySerializer, SubCategorySerializer, \
    ProductFilterSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'characteristic', 'sub_category').all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('sub_categories')
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductFilterViewSet(generics.ListAPIView):
    serializer_class = ProductFilterSerializer

    def get_queryset(self):
        products = Product.objects.filter(category__slug=self.kwargs['category_name']) \
            .select_related('category', 'characteristic', 'sub_category')
        if not products:
            products = Product.objects.filter(sub_category__slug=self.kwargs['category_name']) \
                .select_related('category', 'characteristic', 'sub_category')
        return products
