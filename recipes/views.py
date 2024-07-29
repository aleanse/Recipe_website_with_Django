from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http.response import HttpResponse, Http404
from recipes.models import Recipe, User, Category
from django.contrib import messages
import os
from utils.recipes.pagination import make_pagination
from django.forms.models import model_to_dict
from utils.recipes.factory import make_recipe





def search(request):
    search_term = request.GET.get("q",'').strip()
    if not search_term:
        raise Http404()
    recipe = Recipe.objects.filter(Q(title__icontains=search_term)|Q(description__icontains=search_term),is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipe, 9)
    return render(request, 'recipes/pages/search.html', { 'page_title': f'Search for "{search_term}" |',
                                                          'search_term': search_term,
                                                          'recipes':page_obj,
                                                          'pagination_range': pagination_range,
                                                          'additional_url_query': f'&q={search_term}',})
def home(request):
    recipes = Recipe.objects.filter(is_published=True,).order_by('-id')

    print(Recipe.objects.all())
    

    page_obj, pagination_range = make_pagination(request, recipes, 9)



    return render(request,'recipes/pages/home.html',context={'recipes':page_obj, 'pagination_range': pagination_range})

def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, 9)
    return render(request, 'recipes/pages/category.html', context={ 'recipes':page_obj,'pagination_range': pagination_range, 'title': f'{recipes[0].category.name} - Category | '})


def recipe(request,id):
    recipe = get_object_or_404(Recipe,id=id, is_published=True,)

    return render(request,'recipes/pages/recipe-view.html',context={'recipe':recipe,'is_detail_page': True,})

def search(request):
    search_term = request.GET.get("q",'').strip()
    if not search_term:
        raise Http404()
    recipe = Recipe.objects.filter(Q(title__icontains=search_term)|Q(description__icontains=search_term),is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipe, 9)
    return render(request, 'recipes/pages/search.html', { 'page_title': f'Search for "{search_term}" |',
                                                          'search_term': search_term,
                                                          'recipes':page_obj,
                                                          'pagination_range': pagination_range,
                                                          'additional_url_query': f'&q={search_term}',})
