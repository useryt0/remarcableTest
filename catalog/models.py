from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #on delete set category to null if category is deleted, allow null value (prevents accidental removal of products if category is deleted)
    #category is fk because one product can belong to one category, but one category can have many products
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    #tags is m2m because one product can have many tags, and one tag can belong to many products
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return self.name