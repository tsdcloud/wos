from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'ArticleReference',
            'Designation',
            'UnitPriceHT',
            'Quantity',
            'Packaging',
            'Discount',
            'NetPU',
            'Amount',
        ]


class ProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'ArticleReference',
            'Designation',
            'UnitPriceHT',
            'Quantity',
            'Packaging',
            'Discount',
            'NetPU',
            'Amount',
        ]
