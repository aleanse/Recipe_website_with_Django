from django.urls import path
from recipes import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipes'

urlpatterns = [
    path('', views.home,name="home"),
    path('recipes/search/',views.RecipeListViewSearch.as_view(), name="search"),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/<int:pk>', views.RecipeDetail.as_view(),name="recipe"),
    path('recipes/api/v1',views.RecipeListViewHomeApi.as_view(),name="recipe_api"),
    path('recipes/api/v1/<int:pk>', views.RecipeDetailApi.as_view(), name="recipe_detail_api")



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)