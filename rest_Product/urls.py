from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('reviews', views.ReviewList)
router.register('category', views.Cateqory)
router.register('product', views.Product)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]