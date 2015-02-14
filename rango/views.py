from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


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
        context_dict['slug'] = category_name_slug
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method=='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print (form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			if cat:
				page = form.save(commit=True)
				page.category = cat
				page.views = 0
				page.save()

				return category(request, category_name_slug)
		else:
			print(form.errors)
	else:
		form = PageForm()

	context_dict = {'form': form, 'category': cat}
	return render(request, 'rango/add_page.html', context_dict)


def about(request):

	return render(request, 'rango/about.html')

def register(request):

    #Booleano para decirle al template si el usuario está registrado o no
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #si los 2 formularios son validos
        if user_form.is_valid() and profile_form.is_valid():
            #Guarda los datos de formulario del usuario a la base de datos
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            #Actualizamos la variable par decirle al template que el registro fue exitoso
            registered = True
            return HttpResponseRedirect("/rango/")
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', locals())


def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        #Se verifica si la combinación usernme/password es valida, y crea un objeto User
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Tu cuenta Rango no está disponible!")
        else:
            print("Detalles de login inválidos: {0}, {1}".format(username, password))
            return HttpResponse("Detalles de login suministrados, son inválidos")

    else:
        return render(request, 'rango/login.html', locals())

@login_required
def restricted(request):
    return render(request,"rango/restricted.html" )

@login_required
def login_out(request):
    logout(request)

    return HttpResponseRedirect('/rango/')

