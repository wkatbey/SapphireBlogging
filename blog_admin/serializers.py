from rest_framework import serializers
from blog.models import Category


class NestedCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

    class Meta:
        model = Category
        fields = ['id', 'title']

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    parent = NestedCategorySerializer()

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent']

    def create(self, validated_data):
        parent = Category.objects.get(pk=validated_data['parent']['id'])
        validated_data.pop('parent')
        category = Category.objects.create(**validated_data)
        category.parent = parent

        return category

    def update(self, instance, validated_data):
        print("In update method")
        instance.parent = Category.objects.get(pk=validated_data['parent']['id'])
        instance.title = validated_data['title']
        
        return instance