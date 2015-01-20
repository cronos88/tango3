from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Page


def index(request):

	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	return render(request, 'rango/index.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}

	try:
		#verifica si el nombre de la categoria existe
		category = Category.objects.get(slug = category_name_slug)
		context_dict['category_name'] = category.name
		#recibe todas las paginas asociadas con la categoria dada
		pages = Page.objects.filter(category=category)
		#añade la lista de resultados al contexto del template
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)

def about(request):

	return render(request, 'rango/about.html')



