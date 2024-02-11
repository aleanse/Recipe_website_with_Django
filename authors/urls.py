from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create_register', views.create_register, name='create_register'),
    path('login/',views.login_view, name='login'),
    path('login/create',views.create_login, name='create_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipe/<int:id>/edit', views.DashboardRecipe.as_view(), name='dashboard_recipe_edit'),
    path('dashboard/new_recipe/', views.DashboardRecipe.as_view(), name='dashboard_new_recipe'),
    path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(), name='dashboard_delete_recipe')
]
