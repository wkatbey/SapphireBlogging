from rest_framework import serializers
from blog.models import Category


class NestedCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    parent = NestedCategorySerializer()

    def create(self, validated_data):
        parent = Category.objects.get(pk=validated_data['parent']['id'])
        validated_data.pop('parent')
        category = Category.objects.create(**validated_data)
        category.parent = parent

        return category
