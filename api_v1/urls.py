from django.urls import path

from api_v1 import views

urlpatterns = [
    # добавление рецепта в избранное
    path("favorites/", views.Favorites.as_view(), name="add_favorites"),
    # удаление рецепта из избранного
    path(
        "favorites/<int:recipe_id>/",
        views.Favorites.as_view(),
        name="delete_favorites",
    ),
    # запрос на подписку
    path("subscriptions/", views.Subscribe.as_view(), name="add_follow"),
    # # запрос на отписку
    path(
        "subscriptions/<int:author_id>/",
        views.Subscribe.as_view(),
        name="delete_follow",
    ),
    # # добавление в список покупок
    path("purchases/", views.Purchases.as_view(), name="add_purchases"),
    # удаление из списка покупок
    path(
        "purchases/<int:recipe_id>/",
        views.Purchases.as_view(),
        name="delete_purchases",
    ),
    # автозаполнение поля Ингредиенты при создании нового рецепта
    path("ingredients/", views.Ingredients.as_view(), name="ingredients"),
]
