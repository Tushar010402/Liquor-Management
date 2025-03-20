import uuid
import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from products.models import (
    Category, Brand, Product, ProductImage, 
    ProductVariant, ProductTax
)
from common.jwt_auth import MicroserviceUser

class ProductsAPITest(TestCase):
    """
    Test the products API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test user
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_products', 'add_products', 'change_products']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Create category
        self.category = Category.objects.create(
            tenant_id=self.tenant_id,
            name="Whisky",
            code="WHSK",
            description="Whisky products",
            created_by=self.user_id
        )
        
        # Create brand
        self.brand = Brand.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker",
            code="JW",
            description="Johnnie Walker whisky",
            country_of_origin="Scotland",
            created_by=self.user_id
        )
        
        # Create product
        self.product = Product.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker Black Label",
            code="JW-BL",
            description="Johnnie Walker Black Label whisky",
            category=self.category,
            brand=self.brand,
            barcode="5000267023656",
            is_active=True,
            is_returnable=True,
            min_stock=10,
            max_stock=100,
            reorder_level=20,
            created_by=self.user_id
        )
        
        # Create product image
        self.product_image = ProductImage.objects.create(
            tenant_id=self.tenant_id,
            product=self.product,
            image="products/jw-black-label.jpg",
            is_primary=True,
            created_by=self.user_id
        )
        
        # Create product variant
        self.product_variant = ProductVariant.objects.create(
            tenant_id=self.tenant_id,
            product=self.product,
            name="750ml",
            sku="JW-BL-750",
            barcode="5000267023656",
            price=Decimal('3500.00'),
            cost_price=Decimal('2800.00'),
            mrp=Decimal('3800.00'),
            discount_price=Decimal('3500.00'),
            weight=750,
            weight_unit="ml",
            is_active=True,
            created_by=self.user_id
        )
        
        # Create product tax
        self.product_tax = ProductTax.objects.create(
            tenant_id=self.tenant_id,
            product=self.product,
            tax_name="GST",
            tax_percentage=Decimal('18.00'),
            is_active=True,
            created_by=self.user_id
        )
    
    def test_list_categories(self):
        """
        Test listing categories.
        """
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Whisky')
    
    def test_create_category(self):
        """
        Test creating a category.
        """
        url = reverse('category-list')
        data = {
            'name': 'Vodka',
            'code': 'VODKA',
            'description': 'Vodka products'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Vodka')
        self.assertEqual(response.data['code'], 'VODKA')
        self.assertEqual(response.data['description'], 'Vodka products')
        
        # Check that the category was created in the database
        category = Category.objects.get(code='VODKA')
        self.assertEqual(category.name, 'Vodka')
        self.assertEqual(category.tenant_id, self.tenant_id)
        self.assertEqual(category.created_by, self.user_id)
    
    def test_retrieve_category(self):
        """
        Test retrieving a category.
        """
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Whisky')
        self.assertEqual(response.data['code'], 'WHSK')
    
    def test_update_category(self):
        """
        Test updating a category.
        """
        url = reverse('category-detail', args=[self.category.id])
        data = {
            'name': 'Scotch Whisky',
            'description': 'Scotch whisky products'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Scotch Whisky')
        self.assertEqual(response.data['description'], 'Scotch whisky products')
        
        # Check that the category was updated in the database
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Scotch Whisky')
        self.assertEqual(self.category.description, 'Scotch whisky products')
    
    def test_list_brands(self):
        """
        Test listing brands.
        """
        url = reverse('brand-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Johnnie Walker')
    
    def test_create_brand(self):
        """
        Test creating a brand.
        """
        url = reverse('brand-list')
        data = {
            'name': 'Absolut',
            'code': 'ABS',
            'description': 'Absolut vodka',
            'country_of_origin': 'Sweden'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Absolut')
        self.assertEqual(response.data['code'], 'ABS')
        self.assertEqual(response.data['country_of_origin'], 'Sweden')
        
        # Check that the brand was created in the database
        brand = Brand.objects.get(code='ABS')
        self.assertEqual(brand.name, 'Absolut')
        self.assertEqual(brand.tenant_id, self.tenant_id)
        self.assertEqual(brand.created_by, self.user_id)
    
    def test_retrieve_brand(self):
        """
        Test retrieving a brand.
        """
        url = reverse('brand-detail', args=[self.brand.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Johnnie Walker')
        self.assertEqual(response.data['code'], 'JW')
        self.assertEqual(response.data['country_of_origin'], 'Scotland')
    
    def test_update_brand(self):
        """
        Test updating a brand.
        """
        url = reverse('brand-detail', args=[self.brand.id])
        data = {
            'description': 'Premium Scotch whisky brand',
            'website': 'www.johnniewalker.com'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Premium Scotch whisky brand')
        self.assertEqual(response.data['website'], 'www.johnniewalker.com')
        
        # Check that the brand was updated in the database
        self.brand.refresh_from_db()
        self.assertEqual(self.brand.description, 'Premium Scotch whisky brand')
        self.assertEqual(self.brand.website, 'www.johnniewalker.com')
    
    def test_list_products(self):
        """
        Test listing products.
        """
        url = reverse('product-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Johnnie Walker Black Label')
    
    def test_filter_products_by_category(self):
        """
        Test filtering products by category.
        """
        url = reverse('product-list')
        response = self.client.get(url, {'category': self.category.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], str(self.category.id))
    
    def test_filter_products_by_brand(self):
        """
        Test filtering products by brand.
        """
        url = reverse('product-list')
        response = self.client.get(url, {'brand': self.brand.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['brand'], str(self.brand.id))
    
    def test_create_product(self):
        """
        Test creating a product.
        """
        url = reverse('product-list')
        data = {
            'name': 'Johnnie Walker Red Label',
            'code': 'JW-RL',
            'description': 'Johnnie Walker Red Label whisky',
            'category': str(self.category.id),
            'brand': str(self.brand.id),
            'barcode': '5000267023663',
            'is_active': True,
            'is_returnable': True,
            'min_stock': 10,
            'max_stock': 100,
            'reorder_level': 20
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Johnnie Walker Red Label')
        self.assertEqual(response.data['code'], 'JW-RL')
        self.assertEqual(response.data['category'], str(self.category.id))
        self.assertEqual(response.data['brand'], str(self.brand.id))
        
        # Check that the product was created in the database
        product = Product.objects.get(code='JW-RL')
        self.assertEqual(product.name, 'Johnnie Walker Red Label')
        self.assertEqual(product.tenant_id, self.tenant_id)
        self.assertEqual(product.created_by, self.user_id)
    
    def test_retrieve_product(self):
        """
        Test retrieving a product.
        """
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['code'], 'JW-BL')
        self.assertEqual(response.data['category'], str(self.category.id))
        self.assertEqual(response.data['brand'], str(self.brand.id))
        self.assertEqual(response.data['barcode'], '5000267023656')
        self.assertTrue(response.data['is_active'])
        self.assertTrue(response.data['is_returnable'])
        self.assertEqual(response.data['min_stock'], 10)
        self.assertEqual(response.data['max_stock'], 100)
        self.assertEqual(response.data['reorder_level'], 20)
    
    def test_update_product(self):
        """
        Test updating a product.
        """
        url = reverse('product-detail', args=[self.product.id])
        data = {
            'description': 'Premium blended Scotch whisky',
            'min_stock': 15,
            'max_stock': 120
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Premium blended Scotch whisky')
        self.assertEqual(response.data['min_stock'], 15)
        self.assertEqual(response.data['max_stock'], 120)
        
        # Check that the product was updated in the database
        self.product.refresh_from_db()
        self.assertEqual(self.product.description, 'Premium blended Scotch whisky')
        self.assertEqual(self.product.min_stock, 15)
        self.assertEqual(self.product.max_stock, 120)
    
    def test_list_product_variants(self):
        """
        Test listing product variants.
        """
        url = reverse('productvariant-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], '750ml')
        self.assertEqual(response.data['results'][0]['sku'], 'JW-BL-750')
    
    def test_filter_product_variants_by_product(self):
        """
        Test filtering product variants by product.
        """
        url = reverse('productvariant-list')
        response = self.client.get(url, {'product': self.product.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product'], str(self.product.id))
    
    def test_create_product_variant(self):
        """
        Test creating a product variant.
        """
        url = reverse('productvariant-list')
        data = {
            'product': str(self.product.id),
            'name': '1L',
            'sku': 'JW-BL-1000',
            'barcode': '5000267023670',
            'price': '4500.00',
            'cost_price': '3600.00',
            'mrp': '4800.00',
            'discount_price': '4500.00',
            'weight': 1000,
            'weight_unit': 'ml',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], '1L')
        self.assertEqual(response.data['sku'], 'JW-BL-1000')
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['price'], '4500.00')
        
        # Check that the product variant was created in the database
        variant = ProductVariant.objects.get(sku='JW-BL-1000')
        self.assertEqual(variant.name, '1L')
        self.assertEqual(variant.tenant_id, self.tenant_id)
        self.assertEqual(variant.created_by, self.user_id)
    
    def test_retrieve_product_variant(self):
        """
        Test retrieving a product variant.
        """
        url = reverse('productvariant-detail', args=[self.product_variant.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], '750ml')
        self.assertEqual(response.data['sku'], 'JW-BL-750')
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['price'], '3500.00')
        self.assertEqual(response.data['cost_price'], '2800.00')
        self.assertEqual(response.data['mrp'], '3800.00')
        self.assertEqual(response.data['discount_price'], '3500.00')
        self.assertEqual(response.data['weight'], 750)
        self.assertEqual(response.data['weight_unit'], 'ml')
        self.assertTrue(response.data['is_active'])
    
    def test_update_product_variant(self):
        """
        Test updating a product variant.
        """
        url = reverse('productvariant-detail', args=[self.product_variant.id])
        data = {
            'price': '3600.00',
            'discount_price': '3600.00'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '3600.00')
        self.assertEqual(response.data['discount_price'], '3600.00')
        
        # Check that the product variant was updated in the database
        self.product_variant.refresh_from_db()
        self.assertEqual(self.product_variant.price, Decimal('3600.00'))
        self.assertEqual(self.product_variant.discount_price, Decimal('3600.00'))