"""
Модуль, содержащий сериализаторы для различных моделей.
"""

from django.db.models import Sum, Value

from rest_framework import serializers

from product.models import Access, Lesson, Product, Statistic, User


class StatisticSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Statistic.
    """
    last_viewed_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Statistic
        fields = (
            'time_duration',
            'status',
            'last_viewed_date',
        )


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'name',
            'slug',
            'text',
            'created_at',
            'video_url',
            'video_duration',
            'statistics',
        )

    def get_statistics(self, lesson):
        """
        Задаёт свой метод для получения статистики для данного урока.
        - lesson: Объект урока.
        Возвращает сериализованные данные статистики для данного урока.
        """
        user = self.context.get('user')
        product = self.context.get('product')
        statistics = Statistic.objects.filter(
            lesson=lesson,
            product=product,
            user=user,
        )
        serializer = StatisticSerializer(
            statistics,
            many=True,
        )
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    owner = serializers.StringRelatedField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'text',
            'created_at',
            'owner',
            'lessons',
        )

    def get_lessons(self, product):
        """
        Задаёт свой метод для получения уроков для данного продукта.
        - product: Объект продукта.
        Возвращает сериализованные данные уроков для данного продукта.
        """
        user = self.context.get('user')
        lessons = product.lessons.all()
        serializer = LessonSerializer(
            lessons,
            many=True,
            context={
                'user': user,
                'product': product,
            },
        )
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """
    products = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'products',
        )

    def get_products(self, user):
        """
        Задаёт свой метод для получения продуктов для данного пользователя.
        - user: Объект пользователя.
        Возвращает сериализованные данные продуктов для данного пользователя.
        """
        if not self.context.get('product'):
            user_accesses = Access.objects.filter(
                user=user,
                access_granted=True).order_by('product')
            output = [user_access.product for user_access in user_accesses]
        else:
            output = [self.context['product']]
        context = self.context.copy() if self.context else {}
        context['user'] = user
        product_serializer = ProductSerializer(
            output,
            many=True,
            context=context,
        )
        return product_serializer.data


class MainProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product, используемый для получения
    основной статистики.
    """
    num_lessons_viewed_all_students = serializers.SerializerMethodField()
    num_lessons = serializers.SerializerMethodField()
    time_all_students_spent_seconds = serializers.SerializerMethodField()
    num_students_on_product = serializers.SerializerMethodField()
    product_acquisition_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'num_lessons',
            'num_lessons_viewed_all_students',
            'time_all_students_spent_seconds',
            'num_students_on_product',
            'product_acquisition_percentage',
        )

    def get_num_lessons(self, product):
        """
        Получает количество уроков для данного продукта.
        - product: Объект продукта.
        Возвращает количество уроков.
        """
        return product.lessons.all().count()

    def get_num_lessons_viewed_all_students(self, product):
        """
        Получает количество уроков, которые были просмотрены всеми
        студентами для данного продукта.
        - product: Объект продукта.
        Возвращает количество уроков, просмотренных всеми студентами.
        """
        return Statistic.objects.filter(
            product=product,
            status=True,
        ).count()

    def get_time_all_students_spent_seconds(self, product):
        """
        Получает общее время, которое все студенты провели на данном продукте.
        - product: Объект продукта.
        Возвращает общее время в секундах.
        """
        from django.db.models.functions import Coalesce
        return Statistic.objects.filter(product=product).aggregate(
            total_duration=Coalesce(Sum('time_duration'), Value(0)))[
            'total_duration']

    def get_num_students_on_product(self, product):
        """
        Получает количество студентов, имеющих доступ к данному продукту.
        - product: Объект продукта.
        Возвращает количество студентов.
        """
        self.num_students_on_product = Access.objects.filter(
            product=product,
            access_granted=True,
        ).count()
        return self.num_students_on_product

    def get_product_acquisition_percentage(self, product):
        return self.num_students_on_product / User.objects.all().count() * 100
