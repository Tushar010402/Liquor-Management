# Generated by Django 4.2.10 on 2025-03-25 17:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is active"),
                ),
                ("tenant_id", models.UUIDField(verbose_name="tenant ID")),
                ("shop_id", models.UUIDField(verbose_name="shop ID")),
                (
                    "po_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="PO number"
                    ),
                ),
                ("po_date", models.DateField(verbose_name="PO date")),
                ("supplier_id", models.UUIDField(verbose_name="supplier ID")),
                (
                    "supplier_name",
                    models.CharField(max_length=200, verbose_name="supplier name"),
                ),
                (
                    "supplier_code",
                    models.CharField(max_length=50, verbose_name="supplier code"),
                ),
                (
                    "expected_delivery_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="expected delivery date"
                    ),
                ),
                (
                    "delivery_address",
                    models.TextField(blank=True, verbose_name="delivery address"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("pending", "Pending Approval"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                            ("sent", "Sent to Supplier"),
                            ("partially_received", "Partially Received"),
                            ("received", "Received"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("low", "Low"),
                            ("medium", "Medium"),
                            ("high", "High"),
                        ],
                        default="medium",
                        max_length=20,
                        verbose_name="priority",
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="subtotal"
                    ),
                ),
                (
                    "tax_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="tax amount",
                    ),
                ),
                (
                    "discount_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="discount amount",
                    ),
                ),
                (
                    "shipping_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="shipping amount",
                    ),
                ),
                (
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="total amount"
                    ),
                ),
                (
                    "payment_terms",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="payment terms"
                    ),
                ),
                (
                    "shipping_terms",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="shipping terms"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "internal_notes",
                    models.TextField(blank=True, verbose_name="internal notes"),
                ),
                ("created_by", models.UUIDField(verbose_name="created by")),
                (
                    "approved_by",
                    models.UUIDField(blank=True, null=True, verbose_name="approved by"),
                ),
                (
                    "approved_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="approved at"
                    ),
                ),
                (
                    "rejection_reason",
                    models.TextField(blank=True, verbose_name="rejection reason"),
                ),
                (
                    "is_synced",
                    models.BooleanField(default=True, verbose_name="is synced"),
                ),
                (
                    "sync_id",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="sync ID"
                    ),
                ),
            ],
            options={
                "verbose_name": "purchase order",
                "verbose_name_plural": "purchase orders",
                "ordering": ["-po_date"],
            },
        ),
        migrations.CreateModel(
            name="PurchaseOrderItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is active"),
                ),
                ("tenant_id", models.UUIDField(verbose_name="tenant ID")),
                ("shop_id", models.UUIDField(verbose_name="shop ID")),
                ("product_id", models.UUIDField(verbose_name="product ID")),
                (
                    "product_name",
                    models.CharField(max_length=200, verbose_name="product name"),
                ),
                (
                    "product_code",
                    models.CharField(max_length=50, verbose_name="product code"),
                ),
                (
                    "product_barcode",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="product barcode"
                    ),
                ),
                (
                    "variant_id",
                    models.UUIDField(blank=True, null=True, verbose_name="variant ID"),
                ),
                (
                    "variant_name",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="variant name"
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=3, max_digits=10, verbose_name="quantity"
                    ),
                ),
                (
                    "received_quantity",
                    models.DecimalField(
                        decimal_places=3,
                        default=0,
                        max_digits=10,
                        verbose_name="received quantity",
                    ),
                ),
                (
                    "unit_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="unit price"
                    ),
                ),
                (
                    "tax_rate",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=5,
                        verbose_name="tax rate",
                    ),
                ),
                (
                    "tax_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="tax amount",
                    ),
                ),
                (
                    "discount_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=5,
                        verbose_name="discount percentage",
                    ),
                ),
                (
                    "discount_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="discount amount",
                    ),
                ),
                (
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="total amount"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "purchase_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="purchase_orders.purchaseorder",
                    ),
                ),
            ],
            options={
                "verbose_name": "purchase order item",
                "verbose_name_plural": "purchase order items",
                "ordering": ["product_name"],
            },
        ),
        migrations.CreateModel(
            name="PurchaseOrderHistory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is active"),
                ),
                ("tenant_id", models.UUIDField(verbose_name="tenant ID")),
                ("shop_id", models.UUIDField(verbose_name="shop ID")),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("updated", "Updated"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                            ("sent", "Sent to Supplier"),
                            ("received", "Received"),
                            ("cancelled", "Cancelled"),
                        ],
                        max_length=20,
                        verbose_name="action",
                    ),
                ),
                (
                    "action_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="action date"),
                ),
                ("user_id", models.UUIDField(verbose_name="user ID")),
                (
                    "user_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="user name"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "purchase_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="history",
                        to="purchase_orders.purchaseorder",
                    ),
                ),
            ],
            options={
                "verbose_name": "purchase order history",
                "verbose_name_plural": "purchase order history",
                "ordering": ["-action_date"],
            },
        ),
        migrations.CreateModel(
            name="PurchaseOrderAttachment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is active"),
                ),
                ("tenant_id", models.UUIDField(verbose_name="tenant ID")),
                ("shop_id", models.UUIDField(verbose_name="shop ID")),
                (
                    "file",
                    models.FileField(
                        upload_to="purchase_order_attachments/", verbose_name="file"
                    ),
                ),
                (
                    "file_name",
                    models.CharField(max_length=255, verbose_name="file name"),
                ),
                (
                    "file_type",
                    models.CharField(max_length=100, verbose_name="file type"),
                ),
                ("file_size", models.PositiveIntegerField(verbose_name="file size")),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="description"
                    ),
                ),
                ("uploaded_by", models.UUIDField(verbose_name="uploaded by")),
                (
                    "purchase_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="purchase_orders.purchaseorder",
                    ),
                ),
            ],
            options={
                "verbose_name": "purchase order attachment",
                "verbose_name_plural": "purchase order attachments",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="purchaseorder",
            index=models.Index(
                fields=["tenant_id", "shop_id", "po_date"],
                name="purchase_or_tenant__6a2ad1_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="purchaseorder",
            index=models.Index(
                fields=["tenant_id", "shop_id", "status"],
                name="purchase_or_tenant__b8c3db_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="purchaseorder",
            index=models.Index(
                fields=["tenant_id", "shop_id", "supplier_id"],
                name="purchase_or_tenant__ebb3fb_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="purchaseorder",
            index=models.Index(
                fields=["po_number"], name="purchase_or_po_numb_3289dd_idx"
            ),
        ),
    ]
