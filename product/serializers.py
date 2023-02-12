from rest_framework import serializers
from core.models import Product
from django.utils import timezone


class ProductSerializer(serializers.ModelSerializer):
    """ Serializador para objeto recipe """
    user = serializers.StringRelatedField(read_only=True)
    created = serializers.DateTimeField(default=timezone.now)
    tags = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'price', 'description',
            'slug', 'stock', 'tags', 'image', 'user', 'created', 'updated',
        )
        read_only_fields = ('id',)


class ProductImageSerializer(serializers.ModelSerializer):
    """ Serializador para objeto recipe con imagen """

    class Meta:
        model = Product
        fields = ('id', 'image',)
        read_only_fields = ('id',)
