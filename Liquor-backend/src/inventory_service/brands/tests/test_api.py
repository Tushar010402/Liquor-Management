import uuid
import json
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from brands.models import (
    Brand, BrandCategory, BrandImage, BrandDocument
)
from common.jwt_auth import MicroserviceUser

class BrandsAPITest(TestCase):
    """
    Test the brands API endpoints.
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
            'permissions': ['view_brands', 'add_brands', 'change_brands']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Create brand category
        self.brand_category = BrandCategory.objects.create(
            tenant_id=self.tenant_id,
            name="Premium Whisky",
            code="PWHISKY",
            description="Premium whisky brands",
            created_by=self.user_id
        )
        
        # Create brand
        self.brand = Brand.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker",
            code="JW",
            description="Johnnie Walker whisky",
            brand_category=self.brand_category,
            manufacturer="Diageo",
            country_of_origin="Scotland",
            website="www.johnniewalker.com",
            founded_year=1820,
            status=Brand.STATUS_ACTIVE,
            notes="Premium Scotch whisky brand",
            created_by=self.user_id
        )
        
        # Create brand image
        self.brand_image = BrandImage.objects.create(
            tenant_id=self.tenant_id,
            brand=self.brand,
            image="brands/johnnie_walker_logo.jpg",
            image_type=BrandImage.IMAGE_TYPE_LOGO,
            is_primary=True,
            created_by=self.user_id
        )
        
        # Create brand document
        self.brand_document = BrandDocument.objects.create(
            tenant_id=self.tenant_id,
            brand=self.brand,
            document_type=BrandDocument.DOCUMENT_TYPE_AGREEMENT,
            document_number="AGR123456",
            document_file="brands/jw_agreement.pdf",
            issue_date=date(2023, 1, 1),
            expiry_date=date(2024, 12, 31),
            created_by=self.user_id
        )
    
    def test_list_brand_categories(self):
        """
        Test listing brand categories.
        """
        url = reverse('brandcategory-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Premium Whisky')
        self.assertEqual(response.data['results'][0]['code'], 'PWHISKY')
    
    def test_create_brand_category(self):
        """
        Test creating a brand category.
        """
        url = reverse('brandcategory-list')
        data = {
            'name': 'Premium Vodka',
            'code': 'PVODKA',
            'description': 'Premium vodka brands'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Premium Vodka')
        self.assertEqual(response.data['code'], 'PVODKA')
        self.assertEqual(response.data['description'], 'Premium vodka brands')
        
        # Check that the brand category was created in the database
        category = BrandCategory.objects.get(code='PVODKA')
        self.assertEqual(category.name, 'Premium Vodka')
        self.assertEqual(category.tenant_id, self.tenant_id)
        self.assertEqual(category.created_by, self.user_id)
    
    def test_retrieve_brand_category(self):
        """
        Test retrieving a brand category.
        """
        url = reverse('brandcategory-detail', args=[self.brand_category.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Premium Whisky')
        self.assertEqual(response.data['code'], 'PWHISKY')
        self.assertEqual(response.data['description'], 'Premium whisky brands')
    
    def test_update_brand_category(self):
        """
        Test updating a brand category.
        """
        url = reverse('brandcategory-detail', args=[self.brand_category.id])
        data = {
            'name': 'Super Premium Whisky',
            'description': 'Super premium whisky brands'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Super Premium Whisky')
        self.assertEqual(response.data['description'], 'Super premium whisky brands')
        
        # Check that the brand category was updated in the database
        self.brand_category.refresh_from_db()
        self.assertEqual(self.brand_category.name, 'Super Premium Whisky')
        self.assertEqual(self.brand_category.description, 'Super premium whisky brands')
    
    def test_list_brands(self):
        """
        Test listing brands.
        """
        url = reverse('brand-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Johnnie Walker')
        self.assertEqual(response.data['results'][0]['code'], 'JW')
    
    def test_filter_brands_by_category(self):
        """
        Test filtering brands by category.
        """
        url = reverse('brand-list')
        response = self.client.get(url, {'brand_category': self.brand_category.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['brand_category'], str(self.brand_category.id))
    
    def test_create_brand(self):
        """
        Test creating a brand.
        """
        url = reverse('brand-list')
        data = {
            'name': 'Absolut',
            'code': 'ABS',
            'description': 'Absolut vodka',
            'brand_category': str(self.brand_category.id),
            'manufacturer': 'Pernod Ricard',
            'country_of_origin': 'Sweden',
            'website': 'www.absolut.com',
            'founded_year': 1879,
            'status': Brand.STATUS_ACTIVE,
            'notes': 'Premium vodka brand'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Absolut')
        self.assertEqual(response.data['code'], 'ABS')
        self.assertEqual(response.data['description'], 'Absolut vodka')
        self.assertEqual(response.data['brand_category'], str(self.brand_category.id))
        self.assertEqual(response.data['manufacturer'], 'Pernod Ricard')
        self.assertEqual(response.data['country_of_origin'], 'Sweden')
        self.assertEqual(response.data['website'], 'www.absolut.com')
        self.assertEqual(response.data['founded_year'], 1879)
        self.assertEqual(response.data['status'], Brand.STATUS_ACTIVE)
        self.assertEqual(response.data['notes'], 'Premium vodka brand')
        
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
        self.assertEqual(response.data['description'], 'Johnnie Walker whisky')
        self.assertEqual(response.data['brand_category'], str(self.brand_category.id))
        self.assertEqual(response.data['manufacturer'], 'Diageo')
        self.assertEqual(response.data['country_of_origin'], 'Scotland')
        self.assertEqual(response.data['website'], 'www.johnniewalker.com')
        self.assertEqual(response.data['founded_year'], 1820)
        self.assertEqual(response.data['status'], Brand.STATUS_ACTIVE)
        self.assertEqual(response.data['notes'], 'Premium Scotch whisky brand')
    
    def test_update_brand(self):
        """
        Test updating a brand.
        """
        url = reverse('brand-detail', args=[self.brand.id])
        data = {
            'description': 'Premium blended Scotch whisky',
            'website': 'www.johnniewalker.com/en-us/'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Premium blended Scotch whisky')
        self.assertEqual(response.data['website'], 'www.johnniewalker.com/en-us/')
        
        # Check that the brand was updated in the database
        self.brand.refresh_from_db()
        self.assertEqual(self.brand.description, 'Premium blended Scotch whisky')
        self.assertEqual(self.brand.website, 'www.johnniewalker.com/en-us/')
    
    def test_list_brand_images(self):
        """
        Test listing brand images.
        """
        url = reverse('brandimage-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['image'], 'brands/johnnie_walker_logo.jpg')
        self.assertEqual(response.data['results'][0]['image_type'], BrandImage.IMAGE_TYPE_LOGO)
    
    def test_filter_brand_images_by_brand(self):
        """
        Test filtering brand images by brand.
        """
        url = reverse('brandimage-list')
        response = self.client.get(url, {'brand': self.brand.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['brand'], str(self.brand.id))
    
    def test_create_brand_image(self):
        """
        Test creating a brand image.
        """
        url = reverse('brandimage-list')
        data = {
            'brand': str(self.brand.id),
            'image': 'brands/johnnie_walker_banner.jpg',
            'image_type': BrandImage.IMAGE_TYPE_BANNER,
            'is_primary': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['brand'], str(self.brand.id))
        self.assertEqual(response.data['image'], 'brands/johnnie_walker_banner.jpg')
        self.assertEqual(response.data['image_type'], BrandImage.IMAGE_TYPE_BANNER)
        self.assertFalse(response.data['is_primary'])
        
        # Check that the brand image was created in the database
        image = BrandImage.objects.get(image='brands/johnnie_walker_banner.jpg')
        self.assertEqual(image.brand, self.brand)
        self.assertEqual(image.tenant_id, self.tenant_id)
        self.assertEqual(image.created_by, self.user_id)
    
    def test_retrieve_brand_image(self):
        """
        Test retrieving a brand image.
        """
        url = reverse('brandimage-detail', args=[self.brand_image.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], str(self.brand.id))
        self.assertEqual(response.data['image'], 'brands/johnnie_walker_logo.jpg')
        self.assertEqual(response.data['image_type'], BrandImage.IMAGE_TYPE_LOGO)
        self.assertTrue(response.data['is_primary'])
    
    def test_update_brand_image(self):
        """
        Test updating a brand image.
        """
        url = reverse('brandimage-detail', args=[self.brand_image.id])
        data = {
            'image': 'brands/johnnie_walker_logo_updated.jpg'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['image'], 'brands/johnnie_walker_logo_updated.jpg')
        
        # Check that the brand image was updated in the database
        self.brand_image.refresh_from_db()
        self.assertEqual(self.brand_image.image, 'brands/johnnie_walker_logo_updated.jpg')
    
    def test_list_brand_documents(self):
        """
        Test listing brand documents.
        """
        url = reverse('branddocument-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['document_type'], BrandDocument.DOCUMENT_TYPE_AGREEMENT)
        self.assertEqual(response.data['results'][0]['document_number'], 'AGR123456')
    
    def test_filter_brand_documents_by_brand(self):
        """
        Test filtering brand documents by brand.
        """
        url = reverse('branddocument-list')
        response = self.client.get(url, {'brand': self.brand.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['brand'], str(self.brand.id))
    
    def test_create_brand_document(self):
        """
        Test creating a brand document.
        """
        url = reverse('branddocument-list')
        data = {
            'brand': str(self.brand.id),
            'document_type': BrandDocument.DOCUMENT_TYPE_LICENSE,
            'document_number': 'LIC123456',
            'document_file': 'brands/jw_license.pdf',
            'issue_date': '2023-01-01',
            'expiry_date': '2024-12-31'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['brand'], str(self.brand.id))
        self.assertEqual(response.data['document_type'], BrandDocument.DOCUMENT_TYPE_LICENSE)
        self.assertEqual(response.data['document_number'], 'LIC123456')
        self.assertEqual(response.data['document_file'], 'brands/jw_license.pdf')
        self.assertEqual(response.data['issue_date'], '2023-01-01')
        self.assertEqual(response.data['expiry_date'], '2024-12-31')
        
        # Check that the brand document was created in the database
        document = BrandDocument.objects.get(document_number='LIC123456')
        self.assertEqual(document.brand, self.brand)
        self.assertEqual(document.tenant_id, self.tenant_id)
        self.assertEqual(document.created_by, self.user_id)
    
    def test_retrieve_brand_document(self):
        """
        Test retrieving a brand document.
        """
        url = reverse('branddocument-detail', args=[self.brand_document.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], str(self.brand.id))
        self.assertEqual(response.data['document_type'], BrandDocument.DOCUMENT_TYPE_AGREEMENT)
        self.assertEqual(response.data['document_number'], 'AGR123456')
        self.assertEqual(response.data['document_file'], 'brands/jw_agreement.pdf')
        self.assertEqual(response.data['issue_date'], '2023-01-01')
        self.assertEqual(response.data['expiry_date'], '2024-12-31')
    
    def test_update_brand_document(self):
        """
        Test updating a brand document.
        """
        url = reverse('branddocument-detail', args=[self.brand_document.id])
        data = {
            'expiry_date': '2025-12-31'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expiry_date'], '2025-12-31')
        
        # Check that the brand document was updated in the database
        self.brand_document.refresh_from_db()
        self.assertEqual(self.brand_document.expiry_date, date(2025, 12, 31))