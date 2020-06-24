from django.contrib import admin

from . import models

@admin.register(models.NiniUser)
class NiniUserAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductImage )
class ProductImageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass