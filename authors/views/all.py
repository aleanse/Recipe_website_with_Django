from django.shortcuts import render, redirect
from django.http import Http404
from authors.forms import RegisterForm, Login_Form, AuthorRecipeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from django.urls import reverse










def register_view(request):
    form = RegisterForm(request.session.get('register_form_data'), None)

    return render(request, 'authors/pages/register_view.html', context={'form': form, 'form_action': reverse('authors:create_register'), })


def create_register(request):
    if not request.POST:
        raise Http404
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in')
        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = Login_Form()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:create_login')
    })


def create_login(request):
    if not request.POST:
        raise Http404()

    form = Login_Form(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect('authors:dashboard')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect('authors:login')
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect('authors:login')
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user)

    return render(request, 'authors/pages/dashboard.html', context={'recipes': recipes, })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(is_published=False, author=request.user, pk=id, ).first()
    if not recipe:
        raise Http404()
    form = AuthorRecipeForm(data=request.POST or None, files=request.FILES or None, instance=recipe)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Your recipe was save with success')
        return redirect('authors:dashboard_recipe_edit', id)

    return render(request, 'authors/pages/dashboard_recipe.html', context={'form': form})


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_new_recipe(request):
    form = AuthorRecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Your recipe was created with success')
        return redirect('authors:dashboard')
    return render(request, 'authors/pages/dashboard_new_recipe.html', context={'form': form})


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_delete_recipe(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')
    recipe = Recipe.objects.filter(is_published=False, author=request.user, pk=id, ).first()
    if not recipe:
        raise Http404()


    recipe.delete()
    messages.success(request, 'Deleted successfully.')

    return redirect(reverse('authors:dashboard'))
