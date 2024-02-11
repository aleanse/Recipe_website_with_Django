from django.urls import path
from recipes import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(),name="home"),
    path('recipes/search/',views.RecipeListViewSearch.as_view(), name="search"),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/<int:pk>', views.RecipeDetail.as_view(),name="recipe"),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)