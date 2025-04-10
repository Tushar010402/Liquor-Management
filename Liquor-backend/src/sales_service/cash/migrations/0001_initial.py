# Generated by Django 4.2.10 on 2025-03-25 16:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BankDeposit",
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
                    "deposit_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="deposit number"
                    ),
                ),
                ("deposit_date", models.DateTimeField(verbose_name="deposit date")),
                (
                    "bank_name",
                    models.CharField(max_length=100, verbose_name="bank name"),
                ),
                (
                    "account_number",
                    models.CharField(max_length=50, verbose_name="account number"),
                ),
                (
                    "branch",
                    models.CharField(blank=True, max_length=100, verbose_name="branch"),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="amount"
                    ),
                ),
                (
                    "deposit_method",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("cheque", "Cheque"),
                            ("transfer", "Transfer"),
                        ],
                        default="cash",
                        max_length=20,
                        verbose_name="deposit method",
                    ),
                ),
                (
                    "reference_number",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="reference number"
                    ),
                ),
                (
                    "cheque_number",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="cheque number"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("verified", "Verified"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "receipt_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="deposit_receipts/",
                        verbose_name="receipt image",
                    ),
                ),
                ("created_by", models.UUIDField(verbose_name="created by")),
                (
                    "verified_by",
                    models.UUIDField(blank=True, null=True, verbose_name="verified by"),
                ),
                (
                    "verified_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="verified at"
                    ),
                ),
                (
                    "rejection_reason",
                    models.TextField(blank=True, verbose_name="rejection reason"),
                ),
            ],
            options={
                "verbose_name": "bank deposit",
                "verbose_name_plural": "bank deposits",
                "ordering": ["-deposit_date"],
            },
        ),
        migrations.CreateModel(
            name="CashTransaction",
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
                    "transaction_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="transaction number"
                    ),
                ),
                (
                    "transaction_date",
                    models.DateTimeField(verbose_name="transaction date"),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("sale", "Sale"),
                            ("return", "Return"),
                            ("deposit", "Deposit"),
                            ("expense", "Expense"),
                            ("adjustment", "Adjustment"),
                            ("opening_balance", "Opening Balance"),
                            ("closing_balance", "Closing Balance"),
                        ],
                        max_length=20,
                        verbose_name="transaction type",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="amount"
                    ),
                ),
                (
                    "running_balance",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="running balance"
                    ),
                ),
                (
                    "reference_id",
                    models.UUIDField(
                        blank=True, null=True, verbose_name="reference ID"
                    ),
                ),
                (
                    "reference_type",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="reference type"
                    ),
                ),
                (
                    "reference_number",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="reference number"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                            ("verified", "Verified"),
                        ],
                        default="completed",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                ("created_by", models.UUIDField(verbose_name="created by")),
                (
                    "verified_by",
                    models.UUIDField(blank=True, null=True, verbose_name="verified by"),
                ),
                (
                    "verified_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="verified at"
                    ),
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
                "verbose_name": "cash transaction",
                "verbose_name_plural": "cash transactions",
                "ordering": ["-transaction_date"],
            },
        ),
        migrations.CreateModel(
            name="UPITransaction",
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
                    "transaction_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="transaction number"
                    ),
                ),
                (
                    "transaction_date",
                    models.DateTimeField(verbose_name="transaction date"),
                ),
                ("upi_id", models.CharField(max_length=100, verbose_name="UPI ID")),
                (
                    "payee_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="payee name"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="amount"
                    ),
                ),
                (
                    "reference_number",
                    models.CharField(max_length=100, verbose_name="reference number"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="completed",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "receipt_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="upi_receipts/",
                        verbose_name="receipt image",
                    ),
                ),
                ("created_by", models.UUIDField(verbose_name="created by")),
                (
                    "cash_transaction",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="upi_transaction",
                        to="cash.cashtransaction",
                    ),
                ),
            ],
            options={
                "verbose_name": "UPI transaction",
                "verbose_name_plural": "UPI transactions",
                "ordering": ["-transaction_date"],
            },
        ),
        migrations.CreateModel(
            name="Expense",
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
                    "expense_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="expense number"
                    ),
                ),
                ("expense_date", models.DateTimeField(verbose_name="expense date")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("utilities", "Utilities"),
                            ("rent", "Rent"),
                            ("salaries", "Salaries"),
                            ("maintenance", "Maintenance"),
                            ("supplies", "Supplies"),
                            ("transportation", "Transportation"),
                            ("marketing", "Marketing"),
                            ("miscellaneous", "Miscellaneous"),
                        ],
                        max_length=20,
                        verbose_name="category",
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="amount"
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("upi", "UPI"),
                            ("bank_transfer", "Bank Transfer"),
                            ("cheque", "Cheque"),
                        ],
                        default="cash",
                        max_length=20,
                        verbose_name="payment method",
                    ),
                ),
                (
                    "reference_number",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="reference number"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="approved",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "receipt_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="expense_receipts/",
                        verbose_name="receipt image",
                    ),
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
                    "cash_transaction",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="expense",
                        to="cash.cashtransaction",
                    ),
                ),
            ],
            options={
                "verbose_name": "expense",
                "verbose_name_plural": "expenses",
                "ordering": ["-expense_date"],
            },
        ),
        migrations.CreateModel(
            name="DailySummary",
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
                ("summary_date", models.DateField(verbose_name="summary date")),
                (
                    "opening_balance",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="opening balance"
                    ),
                ),
                (
                    "closing_balance",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="closing balance"
                    ),
                ),
                (
                    "total_sales",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="total sales",
                    ),
                ),
                (
                    "total_returns",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="total returns",
                    ),
                ),
                (
                    "total_expenses",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="total expenses",
                    ),
                ),
                (
                    "total_deposits",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="total deposits",
                    ),
                ),
                (
                    "cash_sales",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="cash sales",
                    ),
                ),
                (
                    "upi_sales",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="UPI sales",
                    ),
                ),
                (
                    "card_sales",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="card sales",
                    ),
                ),
                (
                    "credit_sales",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="credit sales",
                    ),
                ),
                (
                    "expected_balance",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="expected balance"
                    ),
                ),
                (
                    "balance_difference",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="balance difference",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("submitted", "Submitted"),
                            ("verified", "Verified"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                ("created_by", models.UUIDField(verbose_name="created by")),
                (
                    "verified_by",
                    models.UUIDField(blank=True, null=True, verbose_name="verified by"),
                ),
                (
                    "verified_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="verified at"
                    ),
                ),
            ],
            options={
                "verbose_name": "daily summary",
                "verbose_name_plural": "daily summaries",
                "ordering": ["-summary_date"],
                "unique_together": {("tenant_id", "shop_id", "summary_date")},
            },
        ),
        migrations.AddIndex(
            model_name="cashtransaction",
            index=models.Index(
                fields=["tenant_id", "shop_id", "transaction_date"],
                name="cash_cashtr_tenant__a4984d_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="cashtransaction",
            index=models.Index(
                fields=["tenant_id", "shop_id", "transaction_type"],
                name="cash_cashtr_tenant__dbb460_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="cashtransaction",
            index=models.Index(
                fields=["tenant_id", "shop_id", "status"],
                name="cash_cashtr_tenant__16082f_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="cashtransaction",
            index=models.Index(
                fields=["transaction_number"], name="cash_cashtr_transac_3d769c_idx"
            ),
        ),
        migrations.AddField(
            model_name="bankdeposit",
            name="cash_transaction",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bank_deposit",
                to="cash.cashtransaction",
            ),
        ),
    ]
