from django.shortcuts import render
from django.views import generic
from django.core.serializers import serialize
from django.http import JsonResponse

from . import models

# Create your views here.
def ProductList(request):
    food_products     = models.Product.objects.filter(category__title='Food')
    clothing_products = models.Product.objects.filter(category__title='Clothing')

    data = {
        'food_products'    : [],
        'clothing_products': [],
        }
    for product in food_products:
        pd = {
            'id' : product.pk,
            'title' : product.title,
            'can_add_to_cart' : product.can_add_to_cart,
            'main_price' : product.main_price,
            'sell_price' : product.sell_price,
            'percent_off' : product.percent_off
        }
        data['food_products'].append(pd)
    for product in clothing_products:
        pd = {
            'id' : product.pk,
            'title' : product.title,
            'can_add_to_cart' : product.can_add_to_cart,
            'main_price' : product.main_price,
            'sell_price' : product.sell_price,
            'percent_off' : product.percent_off
        }
        data['clothing_products'].append(pd)
    data["user_data"] = {
        "username" : request.user.get_username(),
        "fullname" : request.user.niniuser.fullname
    }
    return JsonResponse(data=data)

def ProductDetail(request, pk):
    product = models.Product.objects.filter(pk=pk).first()
    product.review_count += 1
    product.save()
    if product:
        if product.category.title == 'Food':
            request.user.niniuser.food_reviews += 1
        else:
            request.user.niniuser.clothing_reviews += 1
        request.user.niniuser.save()
        data = {
            'id' : product.pk,
            'title' : product.title,
            'rate'  : product.rate,
            'review_count' : product.review_count,
            'can_add_to_cart' : product.can_add_to_cart,
            'main_price'  : product.main_price,
            'sell_price'  : product.sell_price,
            'percent_off' : product.percent_off,
            'detail'      : product.detail,
            'explanation' : product.explanation,
            # 'category'    : product.category,  
            'gallery_image' : product.images_url,
        }
        
        related_products =  models.Product.objects.filter(category=product.category).order_by('-rate')[:5]
        data["related_products"] = []
        for related in related_products:
            if related != product:
                sgData = {
                        "id"    : related.pk,
                        "title" : related.title,
                        "list_image_url" : related.images_url,
                        "can_add_to_cart": related.can_add_to_cart,
                        "sell_price"     : related.sell_price,
                        "main_price"     : related.main_price,
                    }
                data['related_products'].append(sgData)
        food_reviews     = request.user.niniuser.food_reviews
        clothing_reviews = request.user.niniuser.clothing_reviews
        total_reviews    = food_reviews + clothing_reviews        
        suggested_products = []
        if total_reviews:
            food_suggested = models.Product.objects.filter(category__title='Food').order_by('-rate')[:int(5*(food_reviews/total_reviews))]
            clothing_suggested = models.Product.objects.filter(category__title='Clothing').order_by('-rate')[:int(5*(clothing_reviews/total_reviews))]
            suggested_products.extend(food_suggested)
            suggested_products.extend(clothing_suggested)
        data['suggested_products'] = []
        for suggested in suggested_products:
            if suggested != product:
                sgData = {
                        "id"    : suggested.pk,
                        "title" : suggested.title,
                        "list_image_url" : suggested.images_url,
                        "can_add_to_cart": suggested.can_add_to_cart,
                        "sell_price"     : suggested.sell_price,
                        "main_price"     : suggested.main_price,
                    }
                data['suggested_products'].append(sgData)
        
    else:
        data = {"error" : 'There isn\'t such Product with id {}'.format(pk)}
    data["user_data"] = {
        "username" : request.user.get_username(),
        "fullname" : request.user.niniuser.fullname
    }
    return JsonResponse(data=data)

def ProductReviewList(request, pk):
    product = models.Product.objects.filter(pk=pk)
    if product:
        reviews = models.Review.objects.filter(product=product[0])        
        data = {"reviews" : []}
        for review in reviews:
            review_data = {
                'id'    : review.pk,
                'title' : review.title,
                'rate'  : review.rate,
                'is_buyer'   : review.is_buyer,
                'creator'    : review.creator.fullname,
                'creator_id' : review.creator.pk,
                'positive_likes'  : review.positive_likes, 
                'negative_likes'  : review.negative_likes, 
                'replys' : review.replies, 
            }
            data['reviews'].append(review_data)
    
    return JsonResponse(data=data)