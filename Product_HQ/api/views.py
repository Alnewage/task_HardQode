"""
Модуль, содержащий представления API для работы с продуктами и пользователями.
"""

from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import MainProductSerializer, UserSerializer
from product.models import Access, Product, User


class UserProductsListView(APIView):
    """
    Представление для просмотра списка продуктов пользователя.
    """
    def get(self, request, user_slug):
        """
        Обработчик GET-запроса для получения списка продуктов пользователя.
        - user_slug: Строка - Слаг пользователя.
        Возвращает данные пользователя в виде HTTP-ответа.
        """
        user = get_object_or_404(User, username=user_slug)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserProductsDetailView(APIView):
    """
    Представление для просмотра деталей продукта пользователя.
    """
    def get(self, request, user_slug, product_slug):
        """
        Обработчик GET-запроса для получения деталей продукта пользователя.
        - user_slug: Строка — Слаг пользователя.
        - product_slug: Строка — Слаг продукта.
        Возвращает данные пользователя в виде HTTP-ответа.
        """
        user = get_object_or_404(User, username=user_slug)
        product = get_object_or_404(Product, slug=product_slug)

        access = Access.objects.filter(
            user=user,
            product=product,
            access_granted=True,
        ).exists()

        if not access:
            raise PermissionDenied(
                "У данного пользователя нет доступа к данному продукту")

        serializer = UserSerializer(
            user,
            context={'product': product},
        )
        return Response(serializer.data)


class MainStatisticsView(APIView):
    """
    Представление для получения основной статистики.
    """
    def get(self, request):
        """
        Обработчик GET-запроса для получения основной статистики.
        - request: Объект запроса HTTP.
        Возвращает данные основной статистики в виде HTTP-ответа.
        """
        products = Product.objects.all()
        serializer = MainProductSerializer(products, many=True)
        return Response(serializer.data)
