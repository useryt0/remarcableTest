from django.shortcuts import render

# Create your views here.

from .selectors import get_product_list, get_all_categories, get_all_tags

#function based view to display product list with search and filter functionality
def product_list(request):
    #get parameters from GET request, with default values and stripping whitespace
    search = request.GET.get("search", "").strip()
    category = request.GET.get("category")
    tags = request.GET.getlist("tags")
    
    #get filtered product list using selector function 
    products = get_product_list(search=search, category=category, tags=tags)
    #get all categories and tags to display in filter form
    all_categories = get_all_categories()
    all_tags = get_all_tags()
    
    #build context dict for template rendering
    context = {
        "products": products,
        "all_categories": all_categories,
        "all_tags": all_tags,
        "search": search,
        "selected_category": int(category) if category else None,
        "selected_tags": [int(tag) for tag in tags] if tags else [],
    }
    #return rendered template with context
    return render(request, "catalog/product_list.html", context)