"""
Kafka configuration for the Liquor Management System.
This file defines the Kafka topics and event types used across all services.
"""

# Kafka topics
TOPICS = {
    # User-related events
    'USER_EVENTS': 'user-events',
    
    # Inventory-related events
    'INVENTORY_EVENTS': 'inventory-events',
    'STOCK_ADJUSTMENT_EVENTS': 'stock-adjustment-events',
    'STOCK_TRANSFER_EVENTS': 'stock-transfer-events',
    
    # Sales-related events
    'SALES_EVENTS': 'sales-events',
    'RETURN_EVENTS': 'return-events',
    'CASH_EVENTS': 'cash-events',
    
    # Purchase-related events
    'PURCHASE_EVENTS': 'purchase-events',
    'GOODS_RECEIPT_EVENTS': 'goods-receipt-events',
    'SUPPLIER_EVENTS': 'supplier-events',
    
    # Accounting-related events
    'ACCOUNTING_EVENTS': 'accounting-events',
    'JOURNAL_EVENTS': 'journal-events',
    
    # Reporting-related events
    'REPORTING_EVENTS': 'reporting-events',
    
    # Notification events
    'NOTIFICATION_EVENTS': 'notification-events',
}

# Event types
EVENT_TYPES = {
    # User events
    'USER_CREATED': 'user_created',
    'USER_UPDATED': 'user_updated',
    'USER_DELETED': 'user_deleted',
    'USER_LOGIN': 'user_login',
    'USER_LOGOUT': 'user_logout',
    'PASSWORD_RESET_REQUESTED': 'password_reset_requested',
    'PASSWORD_RESET_COMPLETED': 'password_reset_completed',
    
    # Tenant events
    'TENANT_CREATED': 'tenant_created',
    'TENANT_UPDATED': 'tenant_updated',
    'TENANT_DELETED': 'tenant_deleted',
    
    # Shop events
    'SHOP_CREATED': 'shop_created',
    'SHOP_UPDATED': 'shop_updated',
    'SHOP_DELETED': 'shop_deleted',
    
    # Inventory events
    'PRODUCT_CREATED': 'product_created',
    'PRODUCT_UPDATED': 'product_updated',
    'PRODUCT_DELETED': 'product_deleted',
    'STOCK_ADJUSTED': 'stock_adjusted',
    'STOCK_TRANSFERRED': 'stock_transferred',
    'LOW_STOCK_ALERT': 'low_stock_alert',
    'EXPIRY_ALERT': 'expiry_alert',
    
    # Sales events
    'SALE_CREATED': 'sale_created',
    'SALE_UPDATED': 'sale_updated',
    'SALE_APPROVED': 'sale_approved',
    'SALE_REJECTED': 'sale_rejected',
    'SALE_COMPLETED': 'sale_completed',
    'SALE_CANCELLED': 'sale_cancelled',
    
    # Return events
    'RETURN_CREATED': 'return_created',
    'RETURN_UPDATED': 'return_updated',
    'RETURN_APPROVED': 'return_approved',
    'RETURN_REJECTED': 'return_rejected',
    'RETURN_COMPLETED': 'return_completed',
    'RETURN_CANCELLED': 'return_cancelled',
    
    # Cash events
    'CASH_TRANSACTION_CREATED': 'cash_transaction_created',
    'DEPOSIT_CREATED': 'deposit_created',
    'DEPOSIT_VERIFIED': 'deposit_verified',
    'EXPENSE_CREATED': 'expense_created',
    'EXPENSE_APPROVED': 'expense_approved',
    'DAILY_SUMMARY_CREATED': 'daily_summary_created',
    
    # Purchase events
    'PURCHASE_ORDER_CREATED': 'purchase_order_created',
    'PURCHASE_ORDER_UPDATED': 'purchase_order_updated',
    'PURCHASE_ORDER_APPROVED': 'purchase_order_approved',
    'PURCHASE_ORDER_REJECTED': 'purchase_order_rejected',
    'PURCHASE_ORDER_SENT': 'purchase_order_sent',
    'PURCHASE_ORDER_CANCELLED': 'purchase_order_cancelled',
    
    # Goods receipt events
    'GOODS_RECEIPT_CREATED': 'goods_receipt_created',
    'GOODS_RECEIPT_UPDATED': 'goods_receipt_updated',
    'GOODS_RECEIPT_APPROVED': 'goods_receipt_approved',
    'GOODS_RECEIPT_REJECTED': 'goods_receipt_rejected',
    'GOODS_RECEIPT_COMPLETED': 'goods_receipt_completed',
    
    # Supplier events
    'SUPPLIER_CREATED': 'supplier_created',
    'SUPPLIER_UPDATED': 'supplier_updated',
    'SUPPLIER_DELETED': 'supplier_deleted',
    'SUPPLIER_PAYMENT_CREATED': 'supplier_payment_created',
    'SUPPLIER_INVOICE_CREATED': 'supplier_invoice_created',
    
    # Accounting events
    'JOURNAL_CREATED': 'journal_created',
    'JOURNAL_POSTED': 'journal_posted',
    'JOURNAL_REVERSED': 'journal_reversed',
    'FISCAL_YEAR_CREATED': 'fiscal_year_created',
    'FISCAL_YEAR_CLOSED': 'fiscal_year_closed',
    'ACCOUNTING_PERIOD_CREATED': 'accounting_period_created',
    'ACCOUNTING_PERIOD_CLOSED': 'accounting_period_closed',
    
    # Reporting events
    'REPORT_GENERATED': 'report_generated',
    'REPORT_SCHEDULED': 'report_scheduled',
    
    # Notification events
    'NOTIFICATION_CREATED': 'notification_created',
}

# Event schemas
EVENT_SCHEMAS = {
    # User events
    EVENT_TYPES['USER_CREATED']: {
        'user_id': 'string',
        'email': 'string',
        'tenant_id': 'string',
        'role': 'string',
        'timestamp': 'string'
    },
    EVENT_TYPES['USER_UPDATED']: {
        'user_id': 'string',
        'email': 'string',
        'tenant_id': 'string',
        'updated_fields': 'array',
        'timestamp': 'string'
    },
    EVENT_TYPES['USER_LOGIN']: {
        'user_id': 'string',
        'email': 'string',
        'tenant_id': 'string',
        'timestamp': 'string'
    },
    
    # Inventory events
    EVENT_TYPES['STOCK_ADJUSTED']: {
        'adjustment_id': 'string',
        'shop_id': 'string',
        'tenant_id': 'string',
        'user_id': 'string',
        'products': 'array',
        'timestamp': 'string'
    },
    
    # Sales events
    EVENT_TYPES['SALE_CREATED']: {
        'sale_id': 'string',
        'invoice_number': 'string',
        'shop_id': 'string',
        'tenant_id': 'string',
        'user_id': 'string',
        'total_amount': 'number',
        'timestamp': 'string'
    },
    
    # Purchase events
    EVENT_TYPES['PURCHASE_ORDER_CREATED']: {
        'purchase_order_id': 'string',
        'po_number': 'string',
        'shop_id': 'string',
        'tenant_id': 'string',
        'user_id': 'string',
        'supplier_id': 'string',
        'total_amount': 'number',
        'timestamp': 'string'
    },
}

# Consumer groups
CONSUMER_GROUPS = {
    'AUTH_SERVICE': 'auth-service-group',
    'INVENTORY_SERVICE': 'inventory-service-group',
    'SALES_SERVICE': 'sales-service-group',
    'PURCHASE_SERVICE': 'purchase-service-group',
    'ACCOUNTING_SERVICE': 'accounting-service-group',
    'REPORTING_SERVICE': 'reporting-service-group',
}