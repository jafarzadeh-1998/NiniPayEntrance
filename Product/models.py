from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title        = models.CharField(max_length=100)
    rate         = models.IntegerField()
    review_count = models.IntegerField()
    sell_price   = models.IntegerField()
    main_price   = models.IntegerField()
    detail       = models.CharField(max_length=1000)
    explanation  = models.CharField(max_length=1000)

    def __str__(self):
        return self.title
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image   = models.ImageField(upload_to=None)

    def __str__(self):
        return self.product.title + " - " + str(self.id)


class Review(models.Model):
    title    = models.CharField(max_length=100)
    text     = models.CharField(max_length=1000)
    rate     = models.IntegerField()
    is_buyer = models.BooleanField()
    creator  = models.ForeignKey(User, on_delete=models.SET_NULL)
    positive_likes =  models.IntegerField()
    negative_likes =  models.IntegerField()

    def __str__(self):
        return self.title + " - " + self.user.fullName

class Reply(models.Model):
    review  = models.ForeignKey(Review, on_delete=models.CASCADE)
    text    = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.review.title + " - " + str(self.id)