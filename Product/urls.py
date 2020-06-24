from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ProductList),
    path('<int:pk>/', views.ProductDetail),
    path('review/<int:pk>/', views.ProductReviewList),    
]