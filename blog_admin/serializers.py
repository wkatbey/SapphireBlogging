from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from blog.models import Category


class NestedCategorySerializer(ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

    class Meta: 
        model = Category
        fields = ['id', 'title']


class CategorySerializer(ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    title = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True
    )

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent']
        
    #def create(self, validated_data):
    #    parent_param = validated_data.pop('parent', None)
    #    category = Category.objects.create(**validated_data)
    #    if parent_param is not None:
    #        parent = Category.objects.get(pk=parent_param['id'])
    #        print("Parent", parent.id)
    #        category.parent = parent
     
    #    return category

    #def update(self, instance, validated_data):
    #    parent_param = validated_data.pop('parent', None)

    #    instance.parent = Category.objects.get(pk=validated_data['parent']['id'])
    #    instance.title = validated_data['title']
        
    #    return instance

    def to_representation(self, instance):
        category = super().to_representation(instance)
        category['parent'] = NestedCategorySerializer(instance.parent).data
        return category