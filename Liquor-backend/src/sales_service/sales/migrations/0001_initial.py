# Generated by Django 4.2.10 on 2025-03-25 16:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BatchSale",
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
                    "batch_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="batch number"
                    ),
                ),
                ("batch_date", models.DateTimeField(verbose_name="batch date")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("pending", "Pending Approval"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                (
                    "total_sales",
                    models.IntegerField(default=0, verbose_name="total sales"),
                ),
                (
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        verbose_name="total amount",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
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
            ],
            options={
                "verbose_name": "batch sale",
                "verbose_name_plural": "batch sales",
                "ordering": ["-batch_date"],
            },
        ),
        migrations.CreateModel(
            name="BatchSaleItem",
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
            ],
            options={
                "verbose_name": "batch sale item",
                "verbose_name_plural": "batch sale items",
            },
        ),
        migrations.CreateModel(
            name="Sale",
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
                    "invoice_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="invoice number"
                    ),
                ),
                ("sale_date", models.DateTimeField(verbose_name="sale date")),
                (
                    "customer_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="customer name"
                    ),
                ),
                (
                    "customer_phone",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="customer phone"
                    ),
                ),
                (
                    "customer_address",
                    models.TextField(blank=True, verbose_name="customer address"),
                ),
                (
                    "sale_type",
                    models.CharField(
                        choices=[
                            ("regular", "Regular"),
                            ("wholesale", "Wholesale"),
                            ("special", "Special"),
                        ],
                        default="regular",
                        max_length=20,
                        verbose_name="sale type",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("pending", "Pending Approval"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="subtotal"
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
                    "discount_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=5,
                        verbose_name="discount percentage",
                    ),
                ),
                (
                    "discount_reason",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="discount reason"
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
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="total amount"
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("upi", "UPI"),
                            ("card", "Card"),
                            ("credit", "Credit"),
                            ("mixed", "Mixed"),
                        ],
                        default="cash",
                        max_length=20,
                        verbose_name="payment method",
                    ),
                ),
                (
                    "payment_reference",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="payment reference"
                    ),
                ),
                (
                    "payment_details",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="payment details"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
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
                "verbose_name": "sale",
                "verbose_name_plural": "sales",
                "ordering": ["-sale_date"],
            },
        ),
        migrations.CreateModel(
            name="SaleDraft",
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
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "customer_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="customer name"
                    ),
                ),
                (
                    "customer_phone",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="customer phone"
                    ),
                ),
                (
                    "sale_type",
                    models.CharField(
                        choices=[
                            ("regular", "Regular"),
                            ("wholesale", "Wholesale"),
                            ("special", "Special"),
                        ],
                        default="regular",
                        max_length=20,
                        verbose_name="sale type",
                    ),
                ),
                (
                    "items_data",
                    models.JSONField(default=list, verbose_name="items data"),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="subtotal"
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
                    "discount_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=5,
                        verbose_name="discount percentage",
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
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="total amount"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                ("created_by", models.UUIDField(verbose_name="created by")),
            ],
            options={
                "verbose_name": "sale draft",
                "verbose_name_plural": "sale drafts",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="SalePayment",
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
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("upi", "UPI"),
                            ("card", "Card"),
                            ("credit", "Credit"),
                        ],
                        max_length=20,
                        verbose_name="payment method",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="amount"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                            ("refunded", "Refunded"),
                        ],
                        default="completed",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                (
                    "reference",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="reference"
                    ),
                ),
                (
                    "details",
                    models.JSONField(blank=True, default=dict, verbose_name="details"),
                ),
                ("created_by", models.UUIDField(verbose_name="created by")),
                (
                    "sale",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="sales.sale",
                    ),
                ),
            ],
            options={
                "verbose_name": "sale payment",
                "verbose_name_plural": "sale payments",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="SaleItem",
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
                    "unit_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="unit price"
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
                    "discount_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=5,
                        verbose_name="discount percentage",
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
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="total amount"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "sale",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="sales.sale",
                    ),
                ),
            ],
            options={
                "verbose_name": "sale item",
                "verbose_name_plural": "sale items",
                "ordering": ["product_name"],
            },
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(
                fields=["tenant_id", "shop_id", "sale_date"],
                name="sales_sale_tenant__99e58d_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(
                fields=["tenant_id", "shop_id", "status"],
                name="sales_sale_tenant__a458a1_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(
                fields=["tenant_id", "shop_id", "created_by"],
                name="sales_sale_tenant__0619aa_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(
                fields=["invoice_number"], name="sales_sale_invoice_78d822_idx"
            ),
        ),
        migrations.AddField(
            model_name="batchsaleitem",
            name="batch",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sales",
                to="sales.batchsale",
            ),
        ),
        migrations.AddField(
            model_name="batchsaleitem",
            name="sale",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="batch_items",
                to="sales.sale",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="batchsaleitem",
            unique_together={("batch", "sale")},
        ),
    ]
