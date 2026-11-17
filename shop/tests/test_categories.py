import pytest
from shop.models import Brand, Category, Product


@pytest.mark.django_db
class TestCategoryList:
    def test_get_categories_anonymous(self, api_client):
        response = api_client.get("/api/v1/categories")
        assert response.status_code == 200

    def test_get_categories_returns_correct_count(self, api_client):
        Category.objects.create(name="Дивани")
        Category.objects.create(name="Ліжка")
        response = api_client.get("/api/v1/categories")
        assert len(response.data) == 2

    def test_create_category_authenticated(self, auth_client):
        response = auth_client.post(
            "/api/v1/categories",
            {"name": "Дивани", "description": "М'які меблі"},
            format="json",
        )
        assert response.status_code == 201
        assert Category.objects.filter(name="Дивани").exists()

    def test_create_category_unauthenticated(self, api_client):
        response = api_client.post(
            "/api/v1/categories",
            {"name": "Дивани"},
            format="json",
        )
        assert response.status_code == 401

    def test_create_category_missing_name(self, auth_client):
        response = auth_client.post("/api/v1/categories", {}, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestCategoryDetail:
    def test_get_category_by_id(self, api_client):
        category = Category.objects.create(name="Дивани")
        response = api_client.get(f"/api/v1/categories/{category.pk}")
        assert response.status_code == 200
        assert response.data["name"] == "Дивани"

    def test_get_category_not_found(self, api_client):
        response = api_client.get("/api/v1/categories/9999")
        assert response.status_code == 404

    def test_patch_category_authenticated(self, auth_client):
        category = Category.objects.create(name="Дивани")
        response = auth_client.patch(
            f"/api/v1/categories/{category.pk}",
            {"description": "Оновлений опис"},
            format="json",
        )
        assert response.status_code == 200
        category.refresh_from_db()
        assert category.description == "Оновлений опис"

    def test_patch_category_unauthenticated(self, api_client):
        category = Category.objects.create(name="Дивани")
        response = api_client.patch(
            f"/api/v1/categories/{category.pk}",
            {"description": "Оновлений опис"},
            format="json",
        )
        assert response.status_code == 401

    def test_patch_category_not_found(self, auth_client):
        response = auth_client.patch(
            "/api/v1/categories/9999",
            {"description": "Опис"},
            format="json",
        )
        assert response.status_code == 404

    def test_delete_category_authenticated(self, auth_client):
        category = Category.objects.create(name="Дивани")
        response = auth_client.delete(f"/api/v1/categories/{category.pk}")
        assert response.status_code == 204
        assert not Category.objects.filter(pk=category.pk).exists()

    def test_delete_category_unauthenticated(self, api_client):
        category = Category.objects.create(name="Дивани")
        response = api_client.delete(f"/api/v1/categories/{category.pk}")
        assert response.status_code == 401

    def test_delete_category_not_found(self, auth_client):
        response = auth_client.delete("/api/v1/categories/9999")
        assert response.status_code == 404

    def test_delete_category_with_products_returns_409(self, auth_client):
        category = Category.objects.create(name="Дивани")
        brand = Brand.objects.create(name="JYSK", country="Данія")
        Product.objects.create(
            name="Диван Comfort",
            price="4999.99",
            stock_quantity=5,
            category=category,
            brand=brand,
        )
        response = auth_client.delete(f"/api/v1/categories/{category.pk}")
        assert response.status_code == 409
        assert Category.objects.filter(pk=category.pk).exists()