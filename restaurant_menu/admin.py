from django.contrib import admin
from .models import Item, About

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("meal", "status")
    list_filter = ("status",)
    search_fields = ("meal","description")
    fields = ('meal', 'description', 'price', 'meal_type', 'status', 'author', 'image')


admin.site.register(Item,MenuItemAdmin)
admin.site.register(About)