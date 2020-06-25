from rest_framework import serializers

from . import models

class demoProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['title', 'images_url', 'can_add_to_cart', 'main_price', 'sell_price']

class CategorySerializer(serializers.ModelSerializer):
    top_products = demoProductSerializer(many=True)
    class Meta:
        model = models.Category
        fields = ['title', 'top_products']

class ProductSerializer(serializers.ModelSerializer):
    related_products = demoProductSerializer(many=True)
    class Meta:
        model = models.Product
        fields = ['title', 'rate', 'review_count', 'images_url', 'can_add_to_cart',
                  'main_price', 'sell_price', 'detail', 'explanation', "related_products"]


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.Reply
        fields = ['id', 'text', 'creator', 'creator_fullname']

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'fullname']

class ReviewSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True)
    # creator = CreatorSerializer(many=True)

    class Meta:
        model = models.Review
        fields = ['product', 'title', 'text', 'rate', 'positive_likes', 'negative_likes',
                  'is_buyer', 'creator', 'creator_fullname', 'replies',]
        