from django.db import models
from django.contrib.auth.models import User as djangoUser

class User(models.Model):
    user = models.OneToOneField(djangoUser, on_delete=models.CASCADE)
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

    @property
    def top_products(self):
        return self.product_set.all().order_by('-rate')[: 5]

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
    
    @property
    def related_products(self):
        return Product.objects.filter(category=self.category).order_by('-rate')[:5]

    def __str__(self):
        return self.title + " - " + str(self.category)
    

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
    creator  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    positive_likes =  models.IntegerField()
    negative_likes =  models.IntegerField()
    
    @property
    def creator_fullname(self):
        return self.creator.fullname

    @property
    def replies(self):
        return Reply.objects.filter(review=self.pk)

    def __str__(self):
        return self.title + " - " + self.creator.fullname

class Reply(models.Model):
    review  = models.ForeignKey(Review, on_delete=models.CASCADE)
    text    = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    @property
    def creator_fullname(self):
        return self.creator.fullname


    def __str__(self):
        return self.review.title + " - " + str(self.id)