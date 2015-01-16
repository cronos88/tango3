from django.contrib import admin
from .models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
	
	fields = ['name', 'views', 'likes',]

class PageAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)


