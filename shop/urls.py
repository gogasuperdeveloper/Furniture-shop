from django.urls import path

from shop.views import (
    BrandDetailView,
    BrandListView,
    CategoryDetailView,
    CategoryListView,
    ProductDetailView,
    ProductListView,
)

urlpatterns = [
    path("products", ProductListView.as_view()),
    path("products/<int:pk>", ProductDetailView.as_view()),
    path("categories", CategoryListView.as_view()),
    path("categories/<int:pk>", CategoryDetailView.as_view()),
    path("brands", BrandListView.as_view()),
    path("brands/<int:pk>", BrandDetailView.as_view()),
]
