from rest_framework import serializers
from .models import Permission, Role, RolePermission


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permission model.
    """
    class Meta:
        model = Permission
        fields = [
            'id', 'code', 'name', 'description', 'category',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RolePermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for RolePermission model.
    """
    permission_details = PermissionSerializer(source='permission', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = [
            'id', 'permission', 'permission_details',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for Role model.
    """
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Role
        fields = [
            'id', 'tenant_id', 'name', 'description',
            'is_system_role', 'permissions',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new role.
    """
    permission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Role
        fields = [
            'tenant_id', 'name', 'description',
            'is_system_role', 'permission_ids'
        ]
    
    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        role = Role.objects.create(**validated_data)
        
        # Assign permissions to the role
        for permission_id in permission_ids:
            try:
                permission = Permission.objects.get(id=permission_id)
                RolePermission.objects.create(role=role, permission=permission)
            except Permission.DoesNotExist:
                pass
        
        return role


class RoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a role.
    """
    permission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Role
        fields = [
            'name', 'description', 'is_active', 'permission_ids'
        ]
    
    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', None)
        
        # Update role instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update permissions if provided
        if permission_ids is not None:
            # Remove existing permissions
            RolePermission.objects.filter(role=instance).delete()
            
            # Add new permissions
            for permission_id in permission_ids:
                try:
                    permission = Permission.objects.get(id=permission_id)
                    RolePermission.objects.create(role=instance, permission=permission)
                except Permission.DoesNotExist:
                    pass
        
        return instance


class RolePermissionAssignSerializer(serializers.Serializer):
    """
    Serializer for assigning permissions to a role.
    """
    permission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=True
    )
    
    def validate_permission_ids(self, value):
        # Validate that all permission IDs exist
        for permission_id in value:
            try:
                Permission.objects.get(id=permission_id)
            except Permission.DoesNotExist:
                raise serializers.ValidationError(f"Permission with ID {permission_id} does not exist.")
        return value