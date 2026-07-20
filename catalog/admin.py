from django.contrib import admin

# Register your models here.

from .models import Category, Tag, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'tag_list')
    search_fields = ('name', 'description')
    list_filter = ('category', 'tags')
    #nicer widget for m2m field in admin
    filter_horizontal = ('tags',)
    #prefetch rows for category to optimize performance (n+1 problem solving)
    list_select_related = ('category',)

    #override get_queryset to prefetch tags for performance optimization (n+1 problem solving)
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    #display tag names as comma-separated list in admin
    @admin.display(description='Tags')
    def tag_list(self, obj):
        return ", ".join(t.name for t in obj.tags.all())