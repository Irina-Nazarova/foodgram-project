from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("create/", views.recipe_create, name="recipe_create"),
    path("purchases/", views.purchases_index, name="purchases_index"),
    path(
        "purchases/<int:recipe_id>/",
        views.purchases_delete,
        name="purchases_delete",
    ),
    path("download/", views.download, name="download"),
    path("edit/<int:recipe_id>/", views.recipe_edit, name="recipe_edit"),
    path("delete/<int:recipe_id>/", views.recipe_delete, name="recipe_delete"),
    path(
        "<str:username>/favorites/",
        views.favorite_recipes,
        name="favorite_recipes",
    ),
    path(
        "<str:username>/<int:recipe_id>/",
        views.recipe_view,
        name="recipe_view",
    ),
    path("<str:username>/follow/", views.follow_index, name="follow_index"),
    path("<str:username>/", views.profile, name="profile"),
]
