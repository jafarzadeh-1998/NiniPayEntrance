from django.db import models
from django.contrib.auth.models import User

class NiniUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150, blank=True, null=True)
    food_reviews = models.IntegerField(default=0)
    clothing_reviews = models.IntegerField(default=0)

    def __str__(self):
        return self.fullname

class Category(models.Model):
    CATEGORY = (
        ('food','Food'),
        ('clothing', 'Clothing'),
    )
    title = models.CharField(max_length=50, choices=CATEGORY, unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    category     = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title        = models.CharField(max_length=100)
    rate         = models.IntegerField()
    review_count = models.IntegerField()
    sell_price   = models.IntegerField()
    main_price   = models.IntegerField()
    percent_off  = models.IntegerField()
    detail       = models.CharField(max_length=1000)
    explanation  = models.CharField(max_length=1000)
    can_add_to_cart = models.BooleanField()

    @property
    def images_url(self):
        gallery = ProductImage.objects.filter(product=self.pk)
        urls = []
        for img in gallery:
            urls.append(img.image.url)
        return urls

    def __str__(self):
        return self.title
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image   = models.ImageField()

    def __str__(self):
        return self.product.title + " - " + str(self.id)


class Review(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    text     = models.CharField(max_length=1000)
    rate     = models.IntegerField()
    is_buyer = models.BooleanField()
    creator  = models.ForeignKey(NiniUser, on_delete=models.SET_NULL, null=True)
    positive_likes =  models.IntegerField()
    negative_likes =  models.IntegerField()

    @property
    def replies(self):
        replies = Reply.objects.filter(review=self.pk)
        replies_data = []
        for reply in replies:
            reply_data = {
                'id'   : reply.pk,
                'text' : reply.text,
                'creator'    : reply.creator.fullname,
                'creator_id' : reply.creator.pk,
            }
            replies_data.append(reply_data)
        return replies_data

    def __str__(self):
        return self.title + " - " + self.creator.fullname

class Reply(models.Model):
    review  = models.ForeignKey(Review, on_delete=models.CASCADE)
    text    = models.CharField(max_length=200)
    creator = models.ForeignKey(NiniUser, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.review.title + " - " + str(self.id)