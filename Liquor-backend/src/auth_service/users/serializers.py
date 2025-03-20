from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserShopAssignment, UserPermission

User = get_user_model()


class UserShopAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for user shop assignments.
    """
    class Meta:
        model = UserShopAssignment
        fields = ['id', 'shop_id', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for user custom permissions.
    """
    class Meta:
        model = UserPermission
        fields = ['id', 'permission_key', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    assigned_shops = UserShopAssignmentSerializer(source='shop_assignments', many=True, read_only=True)
    custom_permissions = UserPermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone', 'tenant_id', 'role',
            'is_active', 'date_joined', 'last_login', 'profile_picture',
            'assigned_shops', 'custom_permissions'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone', 'tenant_id', 'role',
            'password', 'confirm_password', 'is_active', 'profile_picture'
        ]
        read_only_fields = ['id']
    
    def validate(self, attrs):
        # Check that passwords match
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        # Remove confirm_password from attrs
        if 'confirm_password' in attrs:
            del attrs['confirm_password']
            
        return attrs
    
    def create(self, validated_data):
        # Extract password
        password = validated_data.pop('password', None)
        
        # Create user
        user = User.objects.create(**validated_data)
        
        # Set password
        if password:
            user.set_password(password)
            user.save()
            
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing user.
    """
    class Meta:
        model = User
        fields = [
            'full_name', 'phone', 'role', 'is_active', 'profile_picture'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        # Check that new passwords match
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})
            
        return attrs


class UserShopAssignmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating user shop assignments.
    """
    class Meta:
        model = UserShopAssignment
        fields = ['shop_id', 'is_primary']
        
    def create(self, validated_data):
        user = self.context['user']
        return UserShopAssignment.objects.create(user=user, **validated_data)


class UserPermissionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating user custom permissions.
    """
    class Meta:
        model = UserPermission
        fields = ['permission_key']
        
    def create(self, validated_data):
        user = self.context['user']
        return UserPermission.objects.create(user=user, **validated_data)