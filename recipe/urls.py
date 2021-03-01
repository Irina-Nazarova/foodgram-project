from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    # страница создания рецепта
    path('create/', views.recipe_create, name='recipe_create'),
    # страница списка покупок
    path('purchases/', views.purchases_index, name='purchases_index'),
    # скачивание списка покупок
    path('download/', views.download, name='download'),
    # удаление рецепта из списка покупок
    path('purchases/<int:recipe_id>', views.purchases_delete, name='purchases_delete'),
    # страница просмотра избранного
    path('<str:username>/favorites/', views.favorite_recipes, name='favorite_recipes'),
    # страница просмотра рецепта
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    # страница просмотра подписок
    path('<str:username>/follow/', views.follow_index, name='follow_index'),
    # страница автора рецептов
    path('<str:username>/', views.profile, name='profile'),
]
