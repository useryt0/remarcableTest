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
    filter_horizontal = ('tags',)
    list_select_related = ('category',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    @admin.display(description='Tags')
    def tag_list(self, obj):
        return ", ".join(t.name for t in obj.tags.all())