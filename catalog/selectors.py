#selector functions for catalog app
from typing import Optional

from .models import Category, Tag, Product
from django.db.models.query import QuerySet

#functions to return all categories, tags, and products
def get_all_categories():
    return Category.objects.all()

def get_all_tags():
    return Tag.objects.all()

def get_all_products():
    return Product.objects.all()

#function to return list of products, filtered by search, category and tags parameters
def get_product_list(*,
    search: Optional[str] = None, #type hints for readability 
    category: Optional[int] = None, 
    tags: Optional[list[int]]=None
    ) -> QuerySet[Product]:
    
    search = (search or "").strip() #guard for whitespace strings and None value, to make sure search skips if whitespace is passed

    #using select_related for category (FK) and prefetch_related for tags (M2M) to optimize performance and avoid n+1 problem
    products = Product.objects.select_related('category').prefetch_related('tags')
    
    #applying filters for each param if provided
    if search:
        products = products.filter(description__icontains=search)
        
    if category:
        products = products.filter(category=category)
    
    if tags:
        products = products.filter(tags__in=tags).distinct()
    
    return products