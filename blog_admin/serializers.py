from rest_framework import serializers
from blog.models import Category

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    parent = serializers.StringRelatedField(many=False)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)