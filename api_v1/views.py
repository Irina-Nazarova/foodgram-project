import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipe.models import Recipe, FavoriteRecipe, Follow, User, Purchase


class Favorites(View):
    """ При необходимости пользователь может добавить/удалить рецепт из избранного """

    def add_favorites(self, request):
        """ добавление в избранное """

        # получаем id рецепта, которого хотим добавить в избранное
        recipe_id = json.loads(request.body)['id']
        # получаем рецепт, который хотим добавить в избранное
        recipe = get_object_or_404(Recipe, id=recipe_id)

        FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete_favorites(self, request, recipe_id):
        """ удаление из избранного """

        # находим рецепт, который хотим удалить
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # удаляем рецепт из избранного текущего пользователя
        FavoriteRecipe.objects.filter(user=request.user, recipe=recipe
                                      ).delete()
        return JsonResponse({'success': True})


class Subscribe(View):
    """ Подписки добавить/удалить """

    def add_follow(self, request):
        """ подписка на пользователя """

        # получаем id пользователя, на которого хотим подписаться
        author_id = json.loads(request.body)['id']
        # получаем пользователя, на которого хотим подписаться
        author = get_object_or_404(User, id=author_id)

        Follow.objects.get_or_create(user=request.user, author=author)
        return JsonResponse({'success': True})

    def delete_follow(self, request, author_id):
        """ отписка от пользователя """

        # находим пользователя, от которого хотим отписаться
        author = get_object_or_404(User, id=author_id)
        # удаляем из подписок фолловера пользователя,
        # от которого хотим отписаться
        Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({'success': True})


class Purchases(View):
    """ Список покупок может добавлять/удалять только его владелец """

    def add_purchases(self, request):
        """ добавление в список покупок """

        # получаем id рецепта,
        # ингредиенты которого хотим добавить в список покупок
        recipe_id = json.loads(request.body)['id']
        # получаем рецепт, ингредиенты которого хотим добавить в список покупок
        recipe = get_object_or_404(Recipe, id=recipe_id)

        Purchase.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete_purchases(self, request, recipe_id):
        """ удаление из списка покупок """

        # находим рецепт, который хотим удалить из списка покупок
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # удаляем искомый рецепт из списка текущего пользователя
        Purchase.objects.filter(user=request.user, recipe=recipe
                                ).delete()

        return JsonResponse({'success': True})

# @login_required
# def download(request):
#     """скачивание списка покупок"""
#     # функция, формирующая список покупок
#     result = generate_shop_list(request)
#     filename = 'shop_list.txt'
#     response = HttpResponse(result, content_type='text/plain')
#     response['Content-Disposition'] = 'attachment; filename={0}'.format(
#                                                                     filename)
#     return response
#
#
# def page_not_found(request, exception):
#     #  переменная exception содержит отладочную информацию,
#     #  выводить её в шаблон пользовательской страницы 404 не нужно
#     return render(request, 'misc/404.html', {'path': request.path}, status=404)
#
#
# def server_error(request):
#     return render(request, 'misc/500.html', status=500)

