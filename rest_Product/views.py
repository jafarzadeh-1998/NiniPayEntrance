from rest_framework import viewsets, views
from rest_framework.response import Response

from . import models, serializer

class Cateqory(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializer.CategorySerializer
    

class Product(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()            
    serializer_class = serializer.ProductSerializer

class ReviewList(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializer.ReviewSerializer