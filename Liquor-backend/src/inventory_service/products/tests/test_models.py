import uuid
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from products.models import (
    Category, Brand, Product, ProductImage, 
    ProductVariant, ProductTax
)

class ProductModelsTest(TestCase):
    """
    Test the product models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
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
    
    def test_category_creation(self):
        """
        Test Category creation.
        """
        self.assertEqual(self.category.name, "Whisky")
        self.assertEqual(self.category.code, "WHSK")
        self.assertEqual(self.category.description, "Whisky products")
        self.assertEqual(self.category.tenant_id, self.tenant_id)
        self.assertEqual(self.category.created_by, self.user_id)
        self.assertTrue(self.category.is_active)
    
    def test_category_str(self):
        """
        Test Category string representation.
        """
        self.assertEqual(str(self.category), "WHSK - Whisky")
    
    def test_brand_creation(self):
        """
        Test Brand creation.
        """
        self.assertEqual(self.brand.name, "Johnnie Walker")
        self.assertEqual(self.brand.code, "JW")
        self.assertEqual(self.brand.description, "Johnnie Walker whisky")
        self.assertEqual(self.brand.country_of_origin, "Scotland")
        self.assertEqual(self.brand.tenant_id, self.tenant_id)
        self.assertEqual(self.brand.created_by, self.user_id)
        self.assertTrue(self.brand.is_active)
    
    def test_brand_str(self):
        """
        Test Brand string representation.
        """
        self.assertEqual(str(self.brand), "JW - Johnnie Walker")
    
    def test_product_creation(self):
        """
        Test Product creation.
        """
        self.assertEqual(self.product.name, "Johnnie Walker Black Label")
        self.assertEqual(self.product.code, "JW-BL")
        self.assertEqual(self.product.description, "Johnnie Walker Black Label whisky")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.brand, self.brand)
        self.assertEqual(self.product.barcode, "5000267023656")
        self.assertTrue(self.product.is_active)
        self.assertTrue(self.product.is_returnable)
        self.assertEqual(self.product.min_stock, 10)
        self.assertEqual(self.product.max_stock, 100)
        self.assertEqual(self.product.reorder_level, 20)
        self.assertEqual(self.product.tenant_id, self.tenant_id)
        self.assertEqual(self.product.created_by, self.user_id)
    
    def test_product_str(self):
        """
        Test Product string representation.
        """
        self.assertEqual(str(self.product), "JW-BL - Johnnie Walker Black Label")
    
    def test_product_image_creation(self):
        """
        Test ProductImage creation.
        """
        self.assertEqual(self.product_image.product, self.product)
        self.assertEqual(self.product_image.image, "products/jw-black-label.jpg")
        self.assertTrue(self.product_image.is_primary)
        self.assertEqual(self.product_image.tenant_id, self.tenant_id)
        self.assertEqual(self.product_image.created_by, self.user_id)
        self.assertTrue(self.product_image.is_active)
    
    def test_product_image_str(self):
        """
        Test ProductImage string representation.
        """
        self.assertEqual(str(self.product_image), "Image for Johnnie Walker Black Label")
    
    def test_product_variant_creation(self):
        """
        Test ProductVariant creation.
        """
        self.assertEqual(self.product_variant.product, self.product)
        self.assertEqual(self.product_variant.name, "750ml")
        self.assertEqual(self.product_variant.sku, "JW-BL-750")
        self.assertEqual(self.product_variant.barcode, "5000267023656")
        self.assertEqual(self.product_variant.price, Decimal('3500.00'))
        self.assertEqual(self.product_variant.cost_price, Decimal('2800.00'))
        self.assertEqual(self.product_variant.mrp, Decimal('3800.00'))
        self.assertEqual(self.product_variant.discount_price, Decimal('3500.00'))
        self.assertEqual(self.product_variant.weight, 750)
        self.assertEqual(self.product_variant.weight_unit, "ml")
        self.assertTrue(self.product_variant.is_active)
        self.assertEqual(self.product_variant.tenant_id, self.tenant_id)
        self.assertEqual(self.product_variant.created_by, self.user_id)
    
    def test_product_variant_str(self):
        """
        Test ProductVariant string representation.
        """
        self.assertEqual(str(self.product_variant), "Johnnie Walker Black Label - 750ml")
    
    def test_product_tax_creation(self):
        """
        Test ProductTax creation.
        """
        self.assertEqual(self.product_tax.product, self.product)
        self.assertEqual(self.product_tax.tax_name, "GST")
        self.assertEqual(self.product_tax.tax_percentage, Decimal('18.00'))
        self.assertTrue(self.product_tax.is_active)
        self.assertEqual(self.product_tax.tenant_id, self.tenant_id)
        self.assertEqual(self.product_tax.created_by, self.user_id)
    
    def test_product_tax_str(self):
        """
        Test ProductTax string representation.
        """
        self.assertEqual(str(self.product_tax), "GST (18.00%) for Johnnie Walker Black Label")