from rest_framework import viewsets, views
from rest_framework.response import Response

from . import models, serializer

class Cateqory(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializer.CategorySerializer
    

class Product(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()            
    serializer_class = serializer.ProductSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            product = models.Product.objects.filter(pk=int(self.kwargs['pk'])).first()
            product.review_count += 1
            product.save()
            if product.category.title == 'food':
                self.request.user.user.food_reviews += 1
                self.request.user.user.save()
            else:
                self.request.user.user.clothing_reviews += 1
                self.request.user.user.save()
        return super().get_serializer_class()


class ReviewList(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializer.ReviewSerializer