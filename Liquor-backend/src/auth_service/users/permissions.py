from rest_framework import permissions


class IsSaasAdmin(permissions.BasePermission):
    """
    Permission to only allow SaaS Admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_saas_admin()


class IsTenantAdmin(permissions.BasePermission):
    """
    Permission to only allow Tenant Admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_tenant_admin()
    
    def has_object_permission(self, request, view, obj):
        # Tenant admins can only access objects in their tenant
        return request.user.tenant_id == getattr(obj, 'tenant_id', None)


class IsUserManager(permissions.BasePermission):
    """
    Permission to only allow Managers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_manager()
    
    def has_object_permission(self, request, view, obj):
        # Managers can only access objects in their tenant
        if request.user.tenant_id != getattr(obj, 'tenant_id', None):
            return False
        
        # Managers can only manage users with lower roles
        if hasattr(obj, 'role'):
            return obj.role in [obj.ROLE_ASSISTANT_MANAGER, obj.ROLE_EXECUTIVE]
        
        return True


class IsAssistantManager(permissions.BasePermission):
    """
    Permission to only allow Assistant Managers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_assistant_manager()
    
    def has_object_permission(self, request, view, obj):
        # Assistant Managers can only access objects in their tenant
        if request.user.tenant_id != getattr(obj, 'tenant_id', None):
            return False
        
        # Assistant Managers can only manage executives
        if hasattr(obj, 'role'):
            return obj.role == obj.ROLE_EXECUTIVE
        
        return True


class IsExecutive(permissions.BasePermission):
    """
    Permission to only allow Executives to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_executive()
    
    def has_object_permission(self, request, view, obj):
        # Executives can only access their own objects
        return getattr(obj, 'id', None) == request.user.id


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission to only allow users to access their own objects,
    or admins to access any object.
    """
    def has_object_permission(self, request, view, obj):
        # Allow if user is accessing their own object
        if getattr(obj, 'id', None) == request.user.id:
            return True
        
        # Allow if user is a SaaS Admin
        if request.user.is_saas_admin():
            return True
        
        # Allow if user is a Tenant Admin and object is in their tenant
        if request.user.is_tenant_admin() and request.user.tenant_id == getattr(obj, 'tenant_id', None):
            return True
        
        return False


class CanManageUsers(permissions.BasePermission):
    """
    Permission to allow users who can manage other users.
    """
    def has_permission(self, request, view):
        # SaaS Admins can manage all users
        if request.user.is_saas_admin():
            return True
        
        # Tenant Admins can manage users in their tenant
        if request.user.is_tenant_admin():
            return True
        
        # Managers can manage assistant managers and executives
        if request.user.is_manager():
            return True
        
        # Assistant Managers can manage executives
        if request.user.is_assistant_manager():
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # SaaS Admins can manage all users
        if request.user.is_saas_admin():
            return True
        
        # Tenant Admins can manage users in their tenant
        if request.user.is_tenant_admin() and request.user.tenant_id == getattr(obj, 'tenant_id', None):
            return True
        
        # Managers can manage assistant managers and executives in their tenant
        if request.user.is_manager() and request.user.tenant_id == getattr(obj, 'tenant_id', None):
            if hasattr(obj, 'role'):
                return obj.role in [obj.ROLE_ASSISTANT_MANAGER, obj.ROLE_EXECUTIVE]
        
        # Assistant Managers can manage executives in their tenant
        if request.user.is_assistant_manager() and request.user.tenant_id == getattr(obj, 'tenant_id', None):
            if hasattr(obj, 'role'):
                return obj.role == obj.ROLE_EXECUTIVE
        
        return False