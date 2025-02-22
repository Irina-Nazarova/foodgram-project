from django.urls import path

from api_v1 import views

urlpatterns = [
    path("favorites/", views.Favorite.as_view(), name="add_favorites"),
    path(
        "favorites/<int:recipe_id>/",
        views.Favorite.as_view(),
        name="delete_favorites",
    ),
    path("subscriptions/", views.Subscribe.as_view(), name="add_follow"),
    path(
        "subscriptions/<int:author_id>/",
        views.Subscribe.as_view(),
        name="delete_follow",
    ),
    path("purchases/", views.ShopingList.as_view(), name="add_purchases"),
    path(
        "purchases/<int:recipe_id>/",
        views.ShopingList.as_view(),
        name="delete_purchases",
    ),
    path("ingredients/", views.AddIngredient.as_view(), name="ingredients"),
]
