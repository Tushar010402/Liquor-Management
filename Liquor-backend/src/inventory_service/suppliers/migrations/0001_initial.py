# Generated by Django 4.2.10 on 2025-03-25 16:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Supplier",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("code", models.CharField(max_length=20, verbose_name="code")),
                (
                    "contact_person",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="contact person"
                    ),
                ),
                (
                    "phone",
                    models.CharField(blank=True, max_length=20, verbose_name="phone"),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="email"),
                ),
                ("website", models.URLField(blank=True, verbose_name="website")),
                ("address", models.TextField(blank=True, verbose_name="address")),
                (
                    "city",
                    models.CharField(blank=True, max_length=100, verbose_name="city"),
                ),
                (
                    "state",
                    models.CharField(blank=True, max_length=100, verbose_name="state"),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="country"
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="postal code"
                    ),
                ),
                (
                    "tax_id",
                    models.CharField(blank=True, max_length=50, verbose_name="tax ID"),
                ),
                (
                    "license_number",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="license number"
                    ),
                ),
                (
                    "license_expiry",
                    models.DateField(
                        blank=True, null=True, verbose_name="license expiry"
                    ),
                ),
                (
                    "payment_terms",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="payment terms"
                    ),
                ),
                (
                    "credit_limit",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="credit limit",
                    ),
                ),
                (
                    "credit_days",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="credit days"
                    ),
                ),
                (
                    "is_approved",
                    models.BooleanField(default=True, verbose_name="is approved"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
            ],
            options={
                "verbose_name": "supplier",
                "verbose_name_plural": "suppliers",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="SupplierDocument",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "document_type",
                    models.CharField(max_length=50, verbose_name="document type"),
                ),
                (
                    "document",
                    models.FileField(
                        upload_to="supplier_documents/", verbose_name="document"
                    ),
                ),
                (
                    "expiry_date",
                    models.DateField(blank=True, null=True, verbose_name="expiry date"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="suppliers.supplier",
                    ),
                ),
            ],
            options={
                "verbose_name": "supplier document",
                "verbose_name_plural": "supplier documents",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="SupplierContact",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "designation",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="designation"
                    ),
                ),
                (
                    "phone",
                    models.CharField(blank=True, max_length=20, verbose_name="phone"),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="email"),
                ),
                (
                    "is_primary",
                    models.BooleanField(default=False, verbose_name="is primary"),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="suppliers.supplier",
                    ),
                ),
            ],
            options={
                "verbose_name": "supplier contact",
                "verbose_name_plural": "supplier contacts",
                "ordering": ["-is_primary", "name"],
            },
        ),
        migrations.CreateModel(
            name="SupplierCategory",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "supplier category",
                "verbose_name_plural": "supplier categories",
                "ordering": ["name"],
                "unique_together": {("tenant_id", "name")},
            },
        ),
        migrations.CreateModel(
            name="SupplierBankAccount",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                (
                    "bank_name",
                    models.CharField(max_length=100, verbose_name="bank name"),
                ),
                (
                    "account_number",
                    models.CharField(max_length=50, verbose_name="account number"),
                ),
                (
                    "account_name",
                    models.CharField(max_length=100, verbose_name="account name"),
                ),
                (
                    "branch",
                    models.CharField(blank=True, max_length=100, verbose_name="branch"),
                ),
                (
                    "ifsc_code",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="IFSC code"
                    ),
                ),
                (
                    "is_primary",
                    models.BooleanField(default=False, verbose_name="is primary"),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bank_accounts",
                        to="suppliers.supplier",
                    ),
                ),
            ],
            options={
                "verbose_name": "supplier bank account",
                "verbose_name_plural": "supplier bank accounts",
                "ordering": ["-is_primary", "bank_name"],
            },
        ),
        migrations.AddField(
            model_name="supplier",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="suppliers",
                to="suppliers.suppliercategory",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="supplier",
            unique_together={("tenant_id", "code")},
        ),
    ]
