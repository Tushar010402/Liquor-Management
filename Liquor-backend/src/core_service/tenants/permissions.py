from rest_framework import permissions


class IsSaasAdmin(permissions.BasePermission):
    """
    Permission to only allow SaaS Admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'saas_admin'


class IsTenantAdmin(permissions.BasePermission):
    """
    Permission to only allow Tenant Admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'tenant_admin'
    
    def has_object_permission(self, request, view, obj):
        # Tenant admins can only access their own tenant
        return str(request.user.tenant_id) == str(getattr(obj, 'id', None))


class IsTenantUser(permissions.BasePermission):
    """
    Permission to only allow users from a specific tenant to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.tenant_id is not None
    
    def has_object_permission(self, request, view, obj):
        # Users can only access objects from their tenant
        return str(request.user.tenant_id) == str(getattr(obj, 'id', None) or getattr(obj, 'tenant_id', None))