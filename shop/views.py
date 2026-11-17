import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Brand, Category, Product
from shop.serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductSerializer,
)

logger = logging.getLogger(__name__)


class CategoryListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        logger.debug("Fetched %d categories", len(serializer.data))
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning("Category creation failed: %s", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info("Category created: %s", serializer.data.get("name"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            logger.warning("Category not found: id=%s", pk)
            return Response({"error": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk):
        category = self.get_object(pk)
        if not category:
            logger.warning("Category update failed, not found: id=%s", pk)
            return Response({"error": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            logger.warning("Category update invalid data: %s", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info("Category updated: id=%s", pk)
        return Response(serializer.data)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            logger.warning("Category delete failed, not found: id=%s", pk)
            return Response({"error": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        product_count = category.products.count()
        if product_count > 0:
            logger.warning("Category delete blocked: id=%s has %d products", pk, product_count)
            return Response(
                {"error": f"Неможливо видалити категорію, оскільки за нею закріплено {product_count} товарів"},
                status=status.HTTP_409_CONFLICT,
            )
        category.delete()
        logger.info("Category deleted: id=%s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        logger.debug("Fetched %d brands", len(serializer.data))
        return Response(serializer.data)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning("Brand creation failed: %s", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info("Brand created: %s", serializer.data.get("name"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return None

    def get(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            logger.warning("Brand not found: id=%s", pk)
            return Response({"error": "Бренд не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    def patch(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            logger.warning("Brand update failed, not found: id=%s", pk)
            return Response({"error": "Бренд не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if not serializer.is_valid():
            logger.warning("Brand update invalid data: %s", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info("Brand updated: id=%s", pk)
        return Response(serializer.data)

    def delete(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            logger.warning("Brand delete failed, not found: id=%s", pk)
            return Response({"error": "Бренд не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        product_count = brand.products.count()
        if product_count > 0:
            logger.warning("Brand delete blocked: id=%s has %d products", pk, product_count)
            return Response(
                {"error": f"Неможливо видалити бренд, оскільки за ним закріплено {product_count} товарів"},
                status=status.HTTP_409_CONFLICT,
            )
        brand.delete()
        logger.info("Brand deleted: id=%s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        search = request.query_params.get("search")
        category_id = request.query_params.get("category_id")
        brand_id = request.query_params.get("brand_id")
        material = request.query_params.get("material")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        sort = request.query_params.get("sort")
        if search:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if category_id:
            products = products.filter(category_id=category_id)
        if brand_id:
            products = products.filter(brand_id=brand_id)
        if material:
            products = products.filter(material__icontains=material)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if sort == "price_asc":
            products = products.order_by("price")
        elif sort == "price_desc":
            products = products.order_by("-price")
        logger.debug("Fetched %d products", products.count())
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning("Product creation failed: %s", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info("Product created: %s", serializer.data.get("name"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            logger.warning("Product not found: id=%s", pk)
            return Response({"error": "Товар не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            logger.warning("Product update failed, not found: id=%s", pk)
            return Response({"error": "Товар не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            logger.warning("Product update invalid data: %s", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info("Product updated: id=%s", pk)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            logger.warning("Product delete failed, not found: id=%s", pk)
            return Response({"error": "Товар не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        logger.info("Product deleted: id=%s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)