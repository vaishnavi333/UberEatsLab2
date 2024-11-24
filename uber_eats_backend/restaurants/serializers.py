from rest_framework import serializers  
from django.contrib.auth.models import User 
from .models import Restaurant, Dish  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Specify the User model to serialize
        fields = ['id', 'username', 'email']  # Define fields to include in the serialized output


class RestaurantSerializer(serializers.ModelSerializer):
    # Define custom serializer fields for formatted opening and closing times
    opening_time = serializers.SerializerMethodField()
    closing_time = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant  # Specify the Restaurant model to serialize
        fields = '__all__'  # Include all fields in the serialized output

    def update(self, instance, validated_data):
        # Preserve the existing image if not provided in the update
        if 'image' not in validated_data:
            validated_data['image'] = instance.image

        # Update other fields
        return super().update(instance, validated_data)
   
    def get_opening_time(self, obj):
        # Custom method to format the opening_time field
        if isinstance(obj.opening_time, str):
            return obj.opening_time  # Return as-is if it's a string
        return obj.opening_time.strftime('%I:%M %p') if obj.opening_time else None  # Format as 12-hour time if it's a TimeField

    def get_closing_time(self, obj):
        # Custom method to format the closing_time field
        if isinstance(obj.closing_time, str):
            return obj.closing_time  # Return as-is if it's a string
        return obj.closing_time.strftime('%I:%M %p') if obj.closing_time else None  # Format as 12-hour time if it's a TimeField


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
        extra_kwargs = {'image': {'required': False}}

    def update(self, instance, validated_data):
        # Preserve the existing image if not provided
        image = validated_data.get('image', None)
        if not image and instance.image:
            validated_data['image'] = instance.image

        # Update other fields
        return super().update(instance, validated_data)
