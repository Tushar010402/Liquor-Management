import uuid
import datetime
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from brands.models import BrandCategory, Brand
from products.models import (
    ProductCategory, ProductType, Product, ProductVariant,
    ProductAttribute, ProductAttributeValue
)
from suppliers.models import SupplierCategory, Supplier, SupplierContact, SupplierBankAccount
from stock.models import StockLevel, StockTransaction

class Command(BaseCommand):
    help = 'Creates test data for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tenant',
            type=str,
            help='Tenant ID to create data for',
            required=True
        )
        parser.add_argument(
            '--shop',
            type=str,
            help='Shop ID to create data for',
            required=True
        )

    def handle(self, *args, **kwargs):
        tenant_id = kwargs['tenant']
        shop_id = kwargs['shop']
        
        self.stdout.write(f'Creating test data for tenant {tenant_id} and shop {shop_id}...')
        
        # Create brand categories
        self.create_brand_categories(tenant_id)
        
        # Create brands
        self.create_brands(tenant_id)
        
        # Create product categories
        self.create_product_categories(tenant_id)
        
        # Create product types
        self.create_product_types(tenant_id)
        
        # Create product attributes
        self.create_product_attributes(tenant_id)
        
        # Create products
        self.create_products(tenant_id)
        
        # Create supplier categories
        self.create_supplier_categories(tenant_id)
        
        # Create suppliers
        self.create_suppliers(tenant_id)
        
        # Create stock levels
        self.create_stock_levels(tenant_id, shop_id)
        
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
    
    def create_brand_categories(self, tenant_id):
        """
        Create brand categories.
        """
        categories = [
            {
                'name': 'Domestic',
                'description': 'Domestic brands'
            },
            {
                'name': 'Imported',
                'description': 'Imported brands'
            },
            {
                'name': 'Premium',
                'description': 'Premium brands'
            },
            {
                'name': 'Budget',
                'description': 'Budget brands'
            },
            {
                'name': 'Craft',
                'description': 'Craft brands'
            }
        ]
        
        for category in categories:
            BrandCategory.objects.get_or_create(
                tenant_id=tenant_id,
                name=category['name'],
                defaults={
                    'description': category['description']
                }
            )
        
        self.stdout.write(f'Created {len(categories)} brand categories')
    
    def create_brands(self, tenant_id):
        """
        Create brands.
        """
        # Get brand categories
        domestic = BrandCategory.objects.get(tenant_id=tenant_id, name='Domestic')
        imported = BrandCategory.objects.get(tenant_id=tenant_id, name='Imported')
        premium = BrandCategory.objects.get(tenant_id=tenant_id, name='Premium')
        budget = BrandCategory.objects.get(tenant_id=tenant_id, name='Budget')
        craft = BrandCategory.objects.get(tenant_id=tenant_id, name='Craft')
        
        brands = [
            {
                'name': 'Royal Stag',
                'code': 'RS',
                'description': 'Royal Stag Whisky',
                'category': domestic,
                'manufacturer': 'Pernod Ricard',
                'country_of_origin': 'India'
            },
            {
                'name': 'Imperial Blue',
                'code': 'IB',
                'description': 'Imperial Blue Whisky',
                'category': domestic,
                'manufacturer': 'Pernod Ricard',
                'country_of_origin': 'India'
            },
            {
                'name': 'Johnnie Walker',
                'code': 'JW',
                'description': 'Johnnie Walker Scotch Whisky',
                'category': imported,
                'manufacturer': 'Diageo',
                'country_of_origin': 'Scotland'
            },
            {
                'name': 'Jack Daniel\'s',
                'code': 'JD',
                'description': 'Jack Daniel\'s Tennessee Whiskey',
                'category': imported,
                'manufacturer': 'Brown-Forman',
                'country_of_origin': 'USA'
            },
            {
                'name': 'Absolut',
                'code': 'ABS',
                'description': 'Absolut Vodka',
                'category': imported,
                'manufacturer': 'Pernod Ricard',
                'country_of_origin': 'Sweden'
            },
            {
                'name': 'Smirnoff',
                'code': 'SMR',
                'description': 'Smirnoff Vodka',
                'category': budget,
                'manufacturer': 'Diageo',
                'country_of_origin': 'Russia'
            },
            {
                'name': 'Bacardi',
                'code': 'BAC',
                'description': 'Bacardi Rum',
                'category': imported,
                'manufacturer': 'Bacardi Limited',
                'country_of_origin': 'Cuba'
            },
            {
                'name': 'Old Monk',
                'code': 'OM',
                'description': 'Old Monk Rum',
                'category': domestic,
                'manufacturer': 'Mohan Meakin',
                'country_of_origin': 'India'
            },
            {
                'name': 'Bombay Sapphire',
                'code': 'BS',
                'description': 'Bombay Sapphire Gin',
                'category': premium,
                'manufacturer': 'Bacardi Limited',
                'country_of_origin': 'England'
            },
            {
                'name': 'Beefeater',
                'code': 'BF',
                'description': 'Beefeater Gin',
                'category': premium,
                'manufacturer': 'Pernod Ricard',
                'country_of_origin': 'England'
            },
            {
                'name': 'Jose Cuervo',
                'code': 'JC',
                'description': 'Jose Cuervo Tequila',
                'category': imported,
                'manufacturer': 'Becle',
                'country_of_origin': 'Mexico'
            },
            {
                'name': 'Kingfisher',
                'code': 'KF',
                'description': 'Kingfisher Beer',
                'category': domestic,
                'manufacturer': 'United Breweries',
                'country_of_origin': 'India'
            },
            {
                'name': 'Heineken',
                'code': 'HNK',
                'description': 'Heineken Beer',
                'category': imported,
                'manufacturer': 'Heineken International',
                'country_of_origin': 'Netherlands'
            },
            {
                'name': 'Bira 91',
                'code': 'BIRA',
                'description': 'Bira 91 Craft Beer',
                'category': craft,
                'manufacturer': 'B9 Beverages',
                'country_of_origin': 'India'
            },
            {
                'name': 'Sula',
                'code': 'SULA',
                'description': 'Sula Wines',
                'category': domestic,
                'manufacturer': 'Sula Vineyards',
                'country_of_origin': 'India'
            }
        ]
        
        for brand in brands:
            Brand.objects.get_or_create(
                tenant_id=tenant_id,
                code=brand['code'],
                defaults={
                    'name': brand['name'],
                    'description': brand['description'],
                    'category': brand['category'],
                    'manufacturer': brand['manufacturer'],
                    'country_of_origin': brand['country_of_origin']
                }
            )
        
        self.stdout.write(f'Created {len(brands)} brands')
    
    def create_product_categories(self, tenant_id):
        """
        Create product categories.
        """
        categories = [
            {
                'name': 'Whisky',
                'description': 'Whisky products',
                'parent': None
            },
            {
                'name': 'Scotch Whisky',
                'description': 'Scotch Whisky products',
                'parent': 'Whisky'
            },
            {
                'name': 'Bourbon Whisky',
                'description': 'Bourbon Whisky products',
                'parent': 'Whisky'
            },
            {
                'name': 'Indian Whisky',
                'description': 'Indian Whisky products',
                'parent': 'Whisky'
            },
            {
                'name': 'Vodka',
                'description': 'Vodka products',
                'parent': None
            },
            {
                'name': 'Flavored Vodka',
                'description': 'Flavored Vodka products',
                'parent': 'Vodka'
            },
            {
                'name': 'Rum',
                'description': 'Rum products',
                'parent': None
            },
            {
                'name': 'Dark Rum',
                'description': 'Dark Rum products',
                'parent': 'Rum'
            },
            {
                'name': 'White Rum',
                'description': 'White Rum products',
                'parent': 'Rum'
            },
            {
                'name': 'Gin',
                'description': 'Gin products',
                'parent': None
            },
            {
                'name': 'Tequila',
                'description': 'Tequila products',
                'parent': None
            },
            {
                'name': 'Beer',
                'description': 'Beer products',
                'parent': None
            },
            {
                'name': 'Lager Beer',
                'description': 'Lager Beer products',
                'parent': 'Beer'
            },
            {
                'name': 'Craft Beer',
                'description': 'Craft Beer products',
                'parent': 'Beer'
            },
            {
                'name': 'Wine',
                'description': 'Wine products',
                'parent': None
            },
            {
                'name': 'Red Wine',
                'description': 'Red Wine products',
                'parent': 'Wine'
            },
            {
                'name': 'White Wine',
                'description': 'White Wine products',
                'parent': 'Wine'
            },
            {
                'name': 'Sparkling Wine',
                'description': 'Sparkling Wine products',
                'parent': 'Wine'
            }
        ]
        
        # First pass: Create all categories
        for category in categories:
            ProductCategory.objects.get_or_create(
                tenant_id=tenant_id,
                name=category['name'],
                defaults={
                    'description': category['description']
                }
            )
        
        # Second pass: Set parent categories
        for category in categories:
            if category['parent']:
                parent = ProductCategory.objects.get(tenant_id=tenant_id, name=category['parent'])
                child = ProductCategory.objects.get(tenant_id=tenant_id, name=category['name'])
                child.parent = parent
                child.save()
        
        self.stdout.write(f'Created {len(categories)} product categories')
    
    def create_product_types(self, tenant_id):
        """
        Create product types.
        """
        types = [
            {
                'name': 'Whisky',
                'description': 'Whisky products'
            },
            {
                'name': 'Vodka',
                'description': 'Vodka products'
            },
            {
                'name': 'Rum',
                'description': 'Rum products'
            },
            {
                'name': 'Gin',
                'description': 'Gin products'
            },
            {
                'name': 'Tequila',
                'description': 'Tequila products'
            },
            {
                'name': 'Beer',
                'description': 'Beer products'
            },
            {
                'name': 'Wine',
                'description': 'Wine products'
            }
        ]
        
        for product_type in types:
            ProductType.objects.get_or_create(
                tenant_id=tenant_id,
                name=product_type['name'],
                defaults={
                    'description': product_type['description']
                }
            )
        
        self.stdout.write(f'Created {len(types)} product types')
    
    def create_product_attributes(self, tenant_id):
        """
        Create product attributes.
        """
        attributes = [
            {
                'name': 'Alcohol Content',
                'description': 'Alcohol content percentage'
            },
            {
                'name': 'Age',
                'description': 'Age of the product'
            },
            {
                'name': 'Color',
                'description': 'Color of the product'
            },
            {
                'name': 'Flavor',
                'description': 'Flavor of the product'
            },
            {
                'name': 'Region',
                'description': 'Region of origin'
            },
            {
                'name': 'Taste Profile',
                'description': 'Taste profile of the product'
            },
            {
                'name': 'Packaging',
                'description': 'Packaging type'
            }
        ]
        
        for attribute in attributes:
            ProductAttribute.objects.get_or_create(
                tenant_id=tenant_id,
                name=attribute['name'],
                defaults={
                    'description': attribute['description']
                }
            )
        
        self.stdout.write(f'Created {len(attributes)} product attributes')
    
    def create_products(self, tenant_id):
        """
        Create products.
        """
        # Get product types
        whisky_type = ProductType.objects.get(tenant_id=tenant_id, name='Whisky')
        vodka_type = ProductType.objects.get(tenant_id=tenant_id, name='Vodka')
        rum_type = ProductType.objects.get(tenant_id=tenant_id, name='Rum')
        gin_type = ProductType.objects.get(tenant_id=tenant_id, name='Gin')
        tequila_type = ProductType.objects.get(tenant_id=tenant_id, name='Tequila')
        beer_type = ProductType.objects.get(tenant_id=tenant_id, name='Beer')
        wine_type = ProductType.objects.get(tenant_id=tenant_id, name='Wine')
        
        # Get product categories
        scotch_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Scotch Whisky')
        bourbon_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Bourbon Whisky')
        indian_whisky_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Indian Whisky')
        vodka_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Vodka')
        flavored_vodka_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Flavored Vodka')
        dark_rum_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Dark Rum')
        white_rum_category = ProductCategory.objects.get(tenant_id=tenant_id, name='White Rum')
        gin_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Gin')
        tequila_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Tequila')
        lager_beer_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Lager Beer')
        craft_beer_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Craft Beer')
        red_wine_category = ProductCategory.objects.get(tenant_id=tenant_id, name='Red Wine')
        white_wine_category = ProductCategory.objects.get(tenant_id=tenant_id, name='White Wine')
        
        # Get brands
        royal_stag = Brand.objects.get(tenant_id=tenant_id, code='RS')
        imperial_blue = Brand.objects.get(tenant_id=tenant_id, code='IB')
        johnnie_walker = Brand.objects.get(tenant_id=tenant_id, code='JW')
        jack_daniels = Brand.objects.get(tenant_id=tenant_id, code='JD')
        absolut = Brand.objects.get(tenant_id=tenant_id, code='ABS')
        smirnoff = Brand.objects.get(tenant_id=tenant_id, code='SMR')
        bacardi = Brand.objects.get(tenant_id=tenant_id, code='BAC')
        old_monk = Brand.objects.get(tenant_id=tenant_id, code='OM')
        bombay_sapphire = Brand.objects.get(tenant_id=tenant_id, code='BS')
        beefeater = Brand.objects.get(tenant_id=tenant_id, code='BF')
        jose_cuervo = Brand.objects.get(tenant_id=tenant_id, code='JC')
        kingfisher = Brand.objects.get(tenant_id=tenant_id, code='KF')
        heineken = Brand.objects.get(tenant_id=tenant_id, code='HNK')
        bira = Brand.objects.get(tenant_id=tenant_id, code='BIRA')
        sula = Brand.objects.get(tenant_id=tenant_id, code='SULA')
        
        # Get product attributes
        alcohol_content = ProductAttribute.objects.get(tenant_id=tenant_id, name='Alcohol Content')
        age = ProductAttribute.objects.get(tenant_id=tenant_id, name='Age')
        color = ProductAttribute.objects.get(tenant_id=tenant_id, name='Color')
        flavor = ProductAttribute.objects.get(tenant_id=tenant_id, name='Flavor')
        region = ProductAttribute.objects.get(tenant_id=tenant_id, name='Region')
        taste_profile = ProductAttribute.objects.get(tenant_id=tenant_id, name='Taste Profile')
        packaging = ProductAttribute.objects.get(tenant_id=tenant_id, name='Packaging')
        
        products = [
            {
                'name': 'Royal Stag Barrel Select',
                'code': 'RS-BS',
                'barcode': '8901234567890',
                'description': 'Royal Stag Barrel Select Whisky',
                'brand': royal_stag,
                'category': indian_whisky_category,
                'product_type': whisky_type,
                'mrp': 1200,
                'selling_price': 1100,
                'purchase_price': 900,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 42.8,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '42.8%'},
                    {'attribute': color, 'value': 'Amber'},
                    {'attribute': region, 'value': 'India'},
                    {'attribute': taste_profile, 'value': 'Smooth, Malty'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': [
                    {
                        'name': '180ml',
                        'code': 'RS-BS-180',
                        'barcode': '8901234567891',
                        'mrp': 300,
                        'selling_price': 280,
                        'purchase_price': 220,
                        'volume_ml': 180
                    },
                    {
                        'name': '375ml',
                        'code': 'RS-BS-375',
                        'barcode': '8901234567892',
                        'mrp': 600,
                        'selling_price': 550,
                        'purchase_price': 450,
                        'volume_ml': 375
                    }
                ]
            },
            {
                'name': 'Imperial Blue',
                'code': 'IB-REG',
                'barcode': '8901234567893',
                'description': 'Imperial Blue Whisky',
                'brand': imperial_blue,
                'category': indian_whisky_category,
                'product_type': whisky_type,
                'mrp': 900,
                'selling_price': 850,
                'purchase_price': 700,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 42.8,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '42.8%'},
                    {'attribute': color, 'value': 'Golden'},
                    {'attribute': region, 'value': 'India'},
                    {'attribute': taste_profile, 'value': 'Smooth, Light'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': [
                    {
                        'name': '180ml',
                        'code': 'IB-REG-180',
                        'barcode': '8901234567894',
                        'mrp': 220,
                        'selling_price': 200,
                        'purchase_price': 160,
                        'volume_ml': 180
                    },
                    {
                        'name': '375ml',
                        'code': 'IB-REG-375',
                        'barcode': '8901234567895',
                        'mrp': 450,
                        'selling_price': 420,
                        'purchase_price': 350,
                        'volume_ml': 375
                    }
                ]
            },
            {
                'name': 'Johnnie Walker Black Label',
                'code': 'JW-BL',
                'barcode': '5000267023656',
                'description': 'Johnnie Walker Black Label Scotch Whisky',
                'brand': johnnie_walker,
                'category': scotch_category,
                'product_type': whisky_type,
                'mrp': 4500,
                'selling_price': 4200,
                'purchase_price': 3500,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 40,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '40%'},
                    {'attribute': age, 'value': '12 Years'},
                    {'attribute': color, 'value': 'Amber'},
                    {'attribute': region, 'value': 'Scotland'},
                    {'attribute': taste_profile, 'value': 'Rich, Complex'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Jack Daniel\'s Old No. 7',
                'code': 'JD-ON7',
                'barcode': '5099873089903',
                'description': 'Jack Daniel\'s Old No. 7 Tennessee Whiskey',
                'brand': jack_daniels,
                'category': bourbon_category,
                'product_type': whisky_type,
                'mrp': 3800,
                'selling_price': 3500,
                'purchase_price': 2800,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 40,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '40%'},
                    {'attribute': color, 'value': 'Amber'},
                    {'attribute': region, 'value': 'Tennessee, USA'},
                    {'attribute': taste_profile, 'value': 'Sweet, Oaky'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Absolut Original',
                'code': 'ABS-ORG',
                'barcode': '7312040017584',
                'description': 'Absolut Original Vodka',
                'brand': absolut,
                'category': vodka_category,
                'product_type': vodka_type,
                'mrp': 2200,
                'selling_price': 2000,
                'purchase_price': 1600,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 40,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '40%'},
                    {'attribute': color, 'value': 'Clear'},
                    {'attribute': region, 'value': 'Sweden'},
                    {'attribute': taste_profile, 'value': 'Clean, Smooth'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Absolut Citron',
                'code': 'ABS-CIT',
                'barcode': '7312040017591',
                'description': 'Absolut Citron Flavored Vodka',
                'brand': absolut,
                'category': flavored_vodka_category,
                'product_type': vodka_type,
                'mrp': 2400,
                'selling_price': 2200,
                'purchase_price': 1800,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 40,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '40%'},
                    {'attribute': color, 'value': 'Clear'},
                    {'attribute': flavor, 'value': 'Lemon'},
                    {'attribute': region, 'value': 'Sweden'},
                    {'attribute': taste_profile, 'value': 'Citrus, Crisp'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Smirnoff No. 21',
                'code': 'SMR-21',
                'barcode': '5410316092417',
                'description': 'Smirnoff No. 21 Vodka',
                'brand': smirnoff,
                'category': vodka_category,
                'product_type': vodka_type,
                'mrp': 1500,
                'selling_price': 1400,
                'purchase_price': 1100,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 37.5,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '37.5%'},
                    {'attribute': color, 'value': 'Clear'},
                    {'attribute': region, 'value': 'Russia'},
                    {'attribute': taste_profile, 'value': 'Clean, Mild'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Bacardi Superior',
                'code': 'BAC-SUP',
                'barcode': '5010677012608',
                'description': 'Bacardi Superior White Rum',
                'brand': bacardi,
                'category': white_rum_category,
                'product_type': rum_type,
                'mrp': 1800,
                'selling_price': 1650,
                'purchase_price': 1300,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 42.8,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '42.8%'},
                    {'attribute': color, 'value': 'Clear'},
                    {'attribute': region, 'value': 'Puerto Rico'},
                    {'attribute': taste_profile, 'value': 'Light, Crisp'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Old Monk Supreme',
                'code': 'OM-SUP',
                'barcode': '8901234567896',
                'description': 'Old Monk Supreme Dark Rum',
                'brand': old_monk,
                'category': dark_rum_category,
                'product_type': rum_type,
                'mrp': 1300,
                'selling_price': 1200,
                'purchase_price': 950,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 42.8,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '42.8%'},
                    {'attribute': color, 'value': 'Dark Brown'},
                    {'attribute': region, 'value': 'India'},
                    {'attribute': taste_profile, 'value': 'Sweet, Vanilla'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Bombay Sapphire',
                'code': 'BS-REG',
                'barcode': '5010677714004',
                'description': 'Bombay Sapphire Gin',
                'brand': bombay_sapphire,
                'category': gin_category,
                'product_type': gin_type,
                'mrp': 2800,
                'selling_price': 2600,
                'purchase_price': 2100,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 40,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '40%'},
                    {'attribute': color, 'value': 'Clear'},
                    {'attribute': region, 'value': 'England'},
                    {'attribute': taste_profile, 'value': 'Botanical, Citrus'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Jose Cuervo Especial Gold',
                'code': 'JC-GOLD',
                'barcode': '7501035042230',
                'description': 'Jose Cuervo Especial Gold Tequila',
                'brand': jose_cuervo,
                'category': tequila_category,
                'product_type': tequila_type,
                'mrp': 2500,
                'selling_price': 2300,
                'purchase_price': 1900,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 38,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '38%'},
                    {'attribute': color, 'value': 'Gold'},
                    {'attribute': region, 'value': 'Mexico'},
                    {'attribute': taste_profile, 'value': 'Sweet, Agave'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Kingfisher Premium',
                'code': 'KF-PREM',
                'barcode': '8901234567897',
                'description': 'Kingfisher Premium Lager Beer',
                'brand': kingfisher,
                'category': lager_beer_category,
                'product_type': beer_type,
                'mrp': 160,
                'selling_price': 150,
                'purchase_price': 120,
                'tax_rate': 18,
                'volume_ml': 650,
                'alcohol_percentage': 4.8,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '4.8%'},
                    {'attribute': color, 'value': 'Golden'},
                    {'attribute': region, 'value': 'India'},
                    {'attribute': taste_profile, 'value': 'Crisp, Light'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': [
                    {
                        'name': '330ml',
                        'code': 'KF-PREM-330',
                        'barcode': '8901234567898',
                        'mrp': 90,
                        'selling_price': 85,
                        'purchase_price': 65,
                        'volume_ml': 330
                    }
                ]
            },
            {
                'name': 'Heineken Lager',
                'code': 'HNK-LAG',
                'barcode': '8901234567899',
                'description': 'Heineken Lager Beer',
                'brand': heineken,
                'category': lager_beer_category,
                'product_type': beer_type,
                'mrp': 200,
                'selling_price': 190,
                'purchase_price': 150,
                'tax_rate': 18,
                'volume_ml': 650,
                'alcohol_percentage': 5,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '5%'},
                    {'attribute': color, 'value': 'Pale Gold'},
                    {'attribute': region, 'value': 'Netherlands'},
                    {'attribute': taste_profile, 'value': 'Crisp, Refreshing'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': [
                    {
                        'name': '330ml',
                        'code': 'HNK-LAG-330',
                        'barcode': '8901234567900',
                        'mrp': 120,
                        'selling_price': 110,
                        'purchase_price': 85,
                        'volume_ml': 330
                    }
                ]
            },
            {
                'name': 'Bira 91 White',
                'code': 'BIRA-WHT',
                'barcode': '8901234567901',
                'description': 'Bira 91 White Ale',
                'brand': bira,
                'category': craft_beer_category,
                'product_type': beer_type,
                'mrp': 180,
                'selling_price': 170,
                'purchase_price': 130,
                'tax_rate': 18,
                'volume_ml': 650,
                'alcohol_percentage': 4.9,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '4.9%'},
                    {'attribute': color, 'value': 'Pale Gold'},
                    {'attribute': region, 'value': 'India'},
                    {'attribute': taste_profile, 'value': 'Citrusy, Wheat'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': [
                    {
                        'name': '330ml',
                        'code': 'BIRA-WHT-330',
                        'barcode': '8901234567902',
                        'mrp': 110,
                        'selling_price': 100,
                        'purchase_price': 75,
                        'volume_ml': 330
                    }
                ]
            },
            {
                'name': 'Sula Shiraz',
                'code': 'SULA-SHZ',
                'barcode': '8901234567903',
                'description': 'Sula Shiraz Red Wine',
                'brand': sula,
                'category': red_wine_category,
                'product_type': wine_type,
                'mrp': 950,
                'selling_price': 900,
                'purchase_price': 700,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 13.5,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '13.5%'},
                    {'attribute': color, 'value': 'Deep Red'},
                    {'attribute': region, 'value': 'Nashik, India'},
                    {'attribute': taste_profile, 'value': 'Fruity, Spicy'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            },
            {
                'name': 'Sula Sauvignon Blanc',
                'code': 'SULA-SB',
                'barcode': '8901234567904',
                'description': 'Sula Sauvignon Blanc White Wine',
                'brand': sula,
                'category': white_wine_category,
                'product_type': wine_type,
                'mrp': 900,
                'selling_price': 850,
                'purchase_price': 650,
                'tax_rate': 18,
                'volume_ml': 750,
                'alcohol_percentage': 12.5,
                'attributes': [
                    {'attribute': alcohol_content, 'value': '12.5%'},
                    {'attribute': color, 'value': 'Pale Yellow'},
                    {'attribute': region, 'value': 'Nashik, India'},
                    {'attribute': taste_profile, 'value': 'Crisp, Citrusy'},
                    {'attribute': packaging, 'value': 'Glass Bottle'}
                ],
                'variants': []
            }
        ]
        
        for product_data in products:
            # Create product
            product, created = Product.objects.get_or_create(
                tenant_id=tenant_id,
                code=product_data['code'],
                defaults={
                    'name': product_data['name'],
                    'barcode': product_data['barcode'],
                    'description': product_data['description'],
                    'brand': product_data['brand'],
                    'category': product_data['category'],
                    'product_type': product_data['product_type'],
                    'mrp': product_data['mrp'],
                    'selling_price': product_data['selling_price'],
                    'purchase_price': product_data['purchase_price'],
                    'tax_rate': product_data['tax_rate'],
                    'volume_ml': product_data['volume_ml'],
                    'alcohol_percentage': product_data['alcohol_percentage']
                }
            )
            
            # Create product attributes
            if created:
                for attr_data in product_data['attributes']:
                    ProductAttributeValue.objects.create(
                        tenant_id=tenant_id,
                        product=product,
                        attribute=attr_data['attribute'],
                        value=attr_data['value']
                    )
                
                # Create product variants
                for variant_data in product_data['variants']:
                    ProductVariant.objects.create(
                        tenant_id=tenant_id,
                        product=product,
                        name=variant_data['name'],
                        code=variant_data['code'],
                        barcode=variant_data['barcode'],
                        mrp=variant_data['mrp'],
                        selling_price=variant_data['selling_price'],
                        purchase_price=variant_data['purchase_price'],
                        volume_ml=variant_data['volume_ml']
                    )
        
        self.stdout.write(f'Created {len(products)} products')
    
    def create_supplier_categories(self, tenant_id):
        """
        Create supplier categories.
        """
        categories = [
            {
                'name': 'Distributor',
                'description': 'Distributors of liquor products'
            },
            {
                'name': 'Wholesaler',
                'description': 'Wholesalers of liquor products'
            },
            {
                'name': 'Manufacturer',
                'description': 'Manufacturers of liquor products'
            },
            {
                'name': 'Importer',
                'description': 'Importers of liquor products'
            }
        ]
        
        for category in categories:
            SupplierCategory.objects.get_or_create(
                tenant_id=tenant_id,
                name=category['name'],
                defaults={
                    'description': category['description']
                }
            )
        
        self.stdout.write(f'Created {len(categories)} supplier categories')
    
    def create_suppliers(self, tenant_id):
        """
        Create suppliers.
        """
        # Get supplier categories
        distributor = SupplierCategory.objects.get(tenant_id=tenant_id, name='Distributor')
        wholesaler = SupplierCategory.objects.get(tenant_id=tenant_id, name='Wholesaler')
        importer = SupplierCategory.objects.get(tenant_id=tenant_id, name='Importer')
        
        suppliers = [
            {
                'name': 'ABC Distributors',
                'code': 'ABC-DIST',
                'category': distributor,
                'contact_person': 'Rajesh Kumar',
                'phone': '9876543210',
                'email': 'rajesh@abcdistributors.com',
                'address': '123 Main Street, Mumbai',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'country': 'India',
                'postal_code': '400001',
                'tax_id': 'GSTIN123456789',
                'payment_terms': 'Net 30',
                'credit_limit': 500000,
                'credit_days': 30,
                'contacts': [
                    {
                        'name': 'Rajesh Kumar',
                        'designation': 'Sales Manager',
                        'phone': '9876543210',
                        'email': 'rajesh@abcdistributors.com',
                        'is_primary': True
                    },
                    {
                        'name': 'Sunil Sharma',
                        'designation': 'Accounts Manager',
                        'phone': '9876543211',
                        'email': 'sunil@abcdistributors.com',
                        'is_primary': False
                    }
                ],
                'bank_accounts': [
                    {
                        'bank_name': 'HDFC Bank',
                        'account_number': '12345678901234',
                        'account_name': 'ABC Distributors',
                        'branch': 'Mumbai Main',
                        'ifsc_code': 'HDFC0001234',
                        'is_primary': True
                    }
                ]
            },
            {
                'name': 'XYZ Wholesalers',
                'code': 'XYZ-WHSL',
                'category': wholesaler,
                'contact_person': 'Priya Patel',
                'phone': '9876543220',
                'email': 'priya@xyzwholesalers.com',
                'address': '456 Park Avenue, Delhi',
                'city': 'Delhi',
                'state': 'Delhi',
                'country': 'India',
                'postal_code': '110001',
                'tax_id': 'GSTIN987654321',
                'payment_terms': 'Net 15',
                'credit_limit': 300000,
                'credit_days': 15,
                'contacts': [
                    {
                        'name': 'Priya Patel',
                        'designation': 'Owner',
                        'phone': '9876543220',
                        'email': 'priya@xyzwholesalers.com',
                        'is_primary': True
                    }
                ],
                'bank_accounts': [
                    {
                        'bank_name': 'ICICI Bank',
                        'account_number': '98765432109876',
                        'account_name': 'XYZ Wholesalers',
                        'branch': 'Delhi Main',
                        'ifsc_code': 'ICIC0001234',
                        'is_primary': True
                    }
                ]
            },
            {
                'name': 'Global Imports',
                'code': 'GLB-IMP',
                'category': importer,
                'contact_person': 'Vikram Singh',
                'phone': '9876543230',
                'email': 'vikram@globalimports.com',
                'address': '789 Central Avenue, Bangalore',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'country': 'India',
                'postal_code': '560001',
                'tax_id': 'GSTIN456789123',
                'payment_terms': 'Net 45',
                'credit_limit': 1000000,
                'credit_days': 45,
                'contacts': [
                    {
                        'name': 'Vikram Singh',
                        'designation': 'CEO',
                        'phone': '9876543230',
                        'email': 'vikram@globalimports.com',
                        'is_primary': True
                    },
                    {
                        'name': 'Anita Desai',
                        'designation': 'Import Manager',
                        'phone': '9876543231',
                        'email': 'anita@globalimports.com',
                        'is_primary': False
                    }
                ],
                'bank_accounts': [
                    {
                        'bank_name': 'State Bank of India',
                        'account_number': '45678912345678',
                        'account_name': 'Global Imports',
                        'branch': 'Bangalore Main',
                        'ifsc_code': 'SBIN0001234',
                        'is_primary': True
                    },
                    {
                        'bank_name': 'Axis Bank',
                        'account_number': '78912345678912',
                        'account_name': 'Global Imports',
                        'branch': 'Bangalore Central',
                        'ifsc_code': 'UTIB0001234',
                        'is_primary': False
                    }
                ]
            }
        ]
        
        for supplier_data in suppliers:
            # Create supplier
            supplier, created = Supplier.objects.get_or_create(
                tenant_id=tenant_id,
                code=supplier_data['code'],
                defaults={
                    'name': supplier_data['name'],
                    'category': supplier_data['category'],
                    'contact_person': supplier_data['contact_person'],
                    'phone': supplier_data['phone'],
                    'email': supplier_data['email'],
                    'address': supplier_data['address'],
                    'city': supplier_data['city'],
                    'state': supplier_data['state'],
                    'country': supplier_data['country'],
                    'postal_code': supplier_data['postal_code'],
                    'tax_id': supplier_data['tax_id'],
                    'payment_terms': supplier_data['payment_terms'],
                    'credit_limit': supplier_data['credit_limit'],
                    'credit_days': supplier_data['credit_days']
                }
            )
            
            # Create supplier contacts
            if created:
                for contact_data in supplier_data['contacts']:
                    SupplierContact.objects.create(
                        tenant_id=tenant_id,
                        supplier=supplier,
                        name=contact_data['name'],
                        designation=contact_data['designation'],
                        phone=contact_data['phone'],
                        email=contact_data['email'],
                        is_primary=contact_data['is_primary']
                    )
                
                # Create supplier bank accounts
                for bank_account_data in supplier_data['bank_accounts']:
                    SupplierBankAccount.objects.create(
                        tenant_id=tenant_id,
                        supplier=supplier,
                        bank_name=bank_account_data['bank_name'],
                        account_number=bank_account_data['account_number'],
                        account_name=bank_account_data['account_name'],
                        branch=bank_account_data['branch'],
                        ifsc_code=bank_account_data['ifsc_code'],
                        is_primary=bank_account_data['is_primary']
                    )
        
        self.stdout.write(f'Created {len(suppliers)} suppliers')
    
    def create_stock_levels(self, tenant_id, shop_id):
        """
        Create stock levels.
        """
        # Get all products
        products = Product.objects.filter(tenant_id=tenant_id)
        
        # Create stock levels for each product
        for product in products:
            # Create stock level for main product
            stock_level, created = StockLevel.objects.get_or_create(
                tenant_id=tenant_id,
                shop_id=shop_id,
                product=product,
                variant=None,
                defaults={
                    'current_stock': random.randint(10, 50),
                    'minimum_stock': 10,
                    'maximum_stock': 100
                }
            )
            
            # Create stock transaction for initial stock
            if created:
                StockTransaction.objects.create(
                    tenant_id=tenant_id,
                    shop_id=shop_id,
                    product=product,
                    variant=None,
                    transaction_type='opening_stock',
                    quantity=stock_level.current_stock,
                    reference_type='initial_setup',
                    notes='Initial stock setup'
                )
            
            # Create stock levels for variants
            for variant in product.variants.all():
                variant_stock_level, variant_created = StockLevel.objects.get_or_create(
                    tenant_id=tenant_id,
                    shop_id=shop_id,
                    product=product,
                    variant=variant,
                    defaults={
                        'current_stock': random.randint(10, 50),
                        'minimum_stock': 10,
                        'maximum_stock': 100
                    }
                )
                
                # Create stock transaction for initial stock
                if variant_created:
                    StockTransaction.objects.create(
                        tenant_id=tenant_id,
                        shop_id=shop_id,
                        product=product,
                        variant=variant,
                        transaction_type='opening_stock',
                        quantity=variant_stock_level.current_stock,
                        reference_type='initial_setup',
                        notes='Initial stock setup'
                    )
        
        self.stdout.write(f'Created stock levels for {products.count()} products')