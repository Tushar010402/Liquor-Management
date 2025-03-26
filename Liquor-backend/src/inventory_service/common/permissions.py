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
        # Tenant admins can only access objects in their tenant
        return str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None))


class IsManager(permissions.BasePermission):
    """
    Permission to only allow Managers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'manager'
    
    def has_object_permission(self, request, view, obj):
        # Managers can only access objects in their tenant
        return str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None))


class IsAssistantManager(permissions.BasePermission):
    """
    Permission to only allow Assistant Managers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'assistant_manager'
    
    def has_object_permission(self, request, view, obj):
        # Assistant Managers can only access objects in their tenant
        return str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None))


class IsExecutive(permissions.BasePermission):
    """
    Permission to only allow Executives to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'executive'
    
    def has_object_permission(self, request, view, obj):
        # Executives can only access objects in their tenant
        return str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None))


class IsTenantUser(permissions.BasePermission):
    """
    Permission to allow any user from a specific tenant to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.tenant_id is not None
    
    def has_object_permission(self, request, view, obj):
        # Users can only access objects in their tenant
        return str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None))


class IsShopUser(permissions.BasePermission):
    """
    Permission to allow users assigned to a specific shop to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.tenant_id is not None
    
    def has_object_permission(self, request, view, obj):
        # Users can only access objects in their tenant and shop
        if str(request.user.tenant_id) != str(getattr(obj, 'tenant_id', None)):
            return False
        
        # Check if the user is assigned to the shop
        # This would require a call to the Auth Service to check shop assignments
        # For now, we'll assume all tenant users can access all shops in their tenant
        return True


class CanManageInventory(permissions.BasePermission):
    """
    Permission to allow users who can manage inventory.
    """
    def has_permission(self, request, view):
        # SaaS Admins can manage all inventory
        if request.user.role == 'saas_admin':
            return True
        
        # Tenant Admins can manage inventory in their tenant
        if request.user.role == 'tenant_admin':
            return True
        
        # Managers can manage inventory in their shops
        if request.user.role == 'manager':
            return True
        
        # Assistant Managers can manage inventory in their shops
        if request.user.role == 'assistant_manager':
            return True
        
        # Executives cannot manage inventory
        return False
    
    def has_object_permission(self, request, view, obj):
        # SaaS Admins can manage all inventory
        if request.user.role == 'saas_admin':
            return True
        
        # Tenant Admins can manage inventory in their tenant
        if request.user.role == 'tenant_admin' and str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None)):
            return True
        
        # Managers can manage inventory in their shops
        if request.user.role == 'manager' and str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None)):
            # Check if the user is assigned to the shop
            # This would require a call to the Auth Service to check shop assignments
            # For now, we'll assume all managers can access all shops in their tenant
            return True
        
        # Assistant Managers can manage inventory in their shops
        if request.user.role == 'assistant_manager' and str(request.user.tenant_id) == str(getattr(obj, 'tenant_id', None)):
            # Check if the user is assigned to the shop
            # This would require a call to the Auth Service to check shop assignments
            # For now, we'll assume all assistant managers can access all shops in their tenant
            return True
        
        return False