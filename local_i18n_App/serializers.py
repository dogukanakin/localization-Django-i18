from rest_framework import serializers
from .models import *
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, use_url=True, required=False)
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content',
                  'description', 'image', 'category',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.name if instance.category else None

    # Update the `image` field in the representation
        return representation

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class MovieNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieName
        fields = ('nameEn', 'nameTr', 'nameAr', 'nameFr', 'year')


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('name_trans',)


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ('language',)
