from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Brand, Category, Product
from shop.serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductSerializer,
)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category)
        data = serializer.data
        data["products"] = ProductSerializer(category.products.all(), many=True).data
        return Response(data)

    def patch(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        count = category.products.count()
        if count > 0:
            return Response(
                {
                    "error": f"Неможливо видалити категорію, оскільки за нею закріплено {count} товарів"
                },
                status=status.HTTP_409_CONFLICT,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandListView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandDetailView(APIView):
    def get(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Бренд не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BrandSerializer(brand)
        data = serializer.data
        data["products"] = ProductSerializer(brand.products.all(), many=True).data
        return Response(data)

    def patch(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Бренд не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Бренд не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        count = brand.products.count()
        if count > 0:
            return Response(
                {
                    "error": f"Неможливо видалити бренд, оскільки за ним закріплено {count} товарів"
                },
                status=status.HTTP_409_CONFLICT,
            )
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()

        search = request.query_params.get("search")
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        category_id = request.query_params.get("category_id")
        if category_id:
            products = products.filter(category_id=category_id)

        brand_id = request.query_params.get("brand_id")
        if brand_id:
            products = products.filter(brand_id=brand_id)

        material = request.query_params.get("material")
        if material:
            products = products.filter(material__icontains=material)

        min_price = request.query_params.get("min_price")
        if min_price:
            products = products.filter(price__gte=min_price)

        max_price = request.query_params.get("max_price")
        if max_price:
            products = products.filter(price__lte=max_price)

        sort = request.query_params.get("sort")
        if sort == "price_asc":
            products = products.order_by("price")
        elif sort == "price_desc":
            products = products.order_by("-price")

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Товар не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Товар не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Товар не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
