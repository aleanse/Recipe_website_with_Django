from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http.response import HttpResponse, Http404
from recipes.models import Recipe, User, Category
from django.contrib import messages
import os
from utils.recipes.pagination import make_pagination
from django.views.generic import DetailView, ListView

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset( *args, **kwargs)
        qs = qs.filter(is_published=True,)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request,ctx.get('recipes'), PER_PAGE)
        ctx.update({'recipes': page_obj, 'pagination_range': pagination_range})

        return ctx

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()
        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        if not search_term:
            raise Http404()
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx

def home(request):
    recipes = Recipe.objects.filter(is_published=True,).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)



    return render(request,'recipes/pages/home.html',context={'recipes':page_obj, 'pagination_range': pagination_range})

def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/category.html', context={ 'recipes':page_obj,'pagination_range': pagination_range, 'title': f'{recipes[0].category.name} - Category | '})


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx
def recipe(request,id):
    recipe = get_object_or_404(Recipe,id=id, is_published=True,)

    return render(request,'recipes/pages/recipe-view.html',context={'recipe':recipe,'is_detail_page': True,})

def search(request):
    search_term = request.GET.get("q",'').strip()
    if not search_term:
        raise Http404()
    recipe = Recipe.objects.filter(Q(title__icontains=search_term)|Q(description__icontains=search_term),is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipe, PER_PAGE)
    return render(request, 'recipes/pages/search.html', { 'page_title': f'Search for "{search_term}" |',
                                                          'search_term': search_term,
                                                          'recipes':page_obj,
                                                          'pagination_range': pagination_range,
                                                          'additional_url_query': f'&q={search_term}',})
