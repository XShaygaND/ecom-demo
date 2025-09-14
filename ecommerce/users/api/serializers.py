from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'date_joined',
            'is_active',
            'is_staff',
            'is_seller',
            'purchases'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'is_staff': {'read_only': True},
            'purchases': {'read_only': True},
        }

    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)

        request = self.context.get('request')
        if request and request.user.is_staff:
            field_names.insert(0, 'id')
            field_names.insert(0, 'url')

        return field_names

    def get_extra_kwargs(self, *args, **kwargs):
        extra_kwargs = super().get_extra_kwargs()

        request = self.context.get('request')
        if request and not request.user.is_staff:
            extra_kwargs.update({
                'is_active': {'read_only': True},
                'is_seller': {'read_only': True},
            })

        return extra_kwargs

    def create(self, validated_data):
        print(validated_data['password'])
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
