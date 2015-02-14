from django.contrib import admin
from .models import Category, Page, UserProfile


class CategoryAdmin(admin.ModelAdmin):
	
	#fields = ['name', 'views', 'likes', 'slug']
	prepopulated_fields = {'slug': ('name',)}

class PageAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)




