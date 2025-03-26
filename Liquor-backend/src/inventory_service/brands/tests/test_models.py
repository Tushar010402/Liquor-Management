import uuid
from django.test import TestCase
from django.utils import timezone
from brands.models import (
    Brand, BrandCategory, BrandImage, BrandDocument
)

class BrandModelsTest(TestCase):
    """
    Test the brand models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
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
            issue_date=timezone.now().date(),
            expiry_date=timezone.now().date() + timezone.timedelta(days=365),
            created_by=self.user_id
        )
    
    def test_brand_category_creation(self):
        """
        Test BrandCategory creation.
        """
        self.assertEqual(self.brand_category.name, "Premium Whisky")
        self.assertEqual(self.brand_category.code, "PWHISKY")
        self.assertEqual(self.brand_category.description, "Premium whisky brands")
        self.assertEqual(self.brand_category.tenant_id, self.tenant_id)
        self.assertEqual(self.brand_category.created_by, self.user_id)
        self.assertTrue(self.brand_category.is_active)
    
    def test_brand_category_str(self):
        """
        Test BrandCategory string representation.
        """
        self.assertEqual(str(self.brand_category), "PWHISKY - Premium Whisky")
    
    def test_brand_creation(self):
        """
        Test Brand creation.
        """
        self.assertEqual(self.brand.name, "Johnnie Walker")
        self.assertEqual(self.brand.code, "JW")
        self.assertEqual(self.brand.description, "Johnnie Walker whisky")
        self.assertEqual(self.brand.brand_category, self.brand_category)
        self.assertEqual(self.brand.manufacturer, "Diageo")
        self.assertEqual(self.brand.country_of_origin, "Scotland")
        self.assertEqual(self.brand.website, "www.johnniewalker.com")
        self.assertEqual(self.brand.founded_year, 1820)
        self.assertEqual(self.brand.status, Brand.STATUS_ACTIVE)
        self.assertEqual(self.brand.notes, "Premium Scotch whisky brand")
        self.assertEqual(self.brand.tenant_id, self.tenant_id)
        self.assertEqual(self.brand.created_by, self.user_id)
        self.assertTrue(self.brand.is_active)
    
    def test_brand_str(self):
        """
        Test Brand string representation.
        """
        self.assertEqual(str(self.brand), "JW - Johnnie Walker")
    
    def test_brand_image_creation(self):
        """
        Test BrandImage creation.
        """
        self.assertEqual(self.brand_image.brand, self.brand)
        self.assertEqual(self.brand_image.image, "brands/johnnie_walker_logo.jpg")
        self.assertEqual(self.brand_image.image_type, BrandImage.IMAGE_TYPE_LOGO)
        self.assertTrue(self.brand_image.is_primary)
        self.assertEqual(self.brand_image.tenant_id, self.tenant_id)
        self.assertEqual(self.brand_image.created_by, self.user_id)
        self.assertTrue(self.brand_image.is_active)
    
    def test_brand_image_str(self):
        """
        Test BrandImage string representation.
        """
        self.assertEqual(str(self.brand_image), "Logo for Johnnie Walker")
    
    def test_brand_document_creation(self):
        """
        Test BrandDocument creation.
        """
        self.assertEqual(self.brand_document.brand, self.brand)
        self.assertEqual(self.brand_document.document_type, BrandDocument.DOCUMENT_TYPE_AGREEMENT)
        self.assertEqual(self.brand_document.document_number, "AGR123456")
        self.assertEqual(self.brand_document.document_file, "brands/jw_agreement.pdf")
        self.assertIsNotNone(self.brand_document.issue_date)
        self.assertIsNotNone(self.brand_document.expiry_date)
        self.assertEqual(self.brand_document.tenant_id, self.tenant_id)
        self.assertEqual(self.brand_document.created_by, self.user_id)
        self.assertTrue(self.brand_document.is_active)
    
    def test_brand_document_str(self):
        """
        Test BrandDocument string representation.
        """
        self.assertEqual(str(self.brand_document), "Agreement - AGR123456")