"""
Этот модуль содержит модели для управления продуктами, уроками,
доступом и статистикой в приложении.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from rest_framework.exceptions import ValidationError

User = get_user_model()


class Product(models.Model):
    """
    Представляет продукт в приложении.

    Поля:
    - name: CharField - Название продукта.
    - slug: SlugField - Идентификатор продукта, используемый в URL.
    - text: TextField - Описание продукта.
    - created_at: DateTimeField - Дата и время публикации продукта.
    - owner: ForeignKey - Владелец продукта.
    - lessons: ManyToManyField - Уроки, связанные с продуктом.
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        unique=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.',
    )
    text = models.TextField(verbose_name='Описание продукта', )
    created_at = models.DateTimeField(
        verbose_name='Дата и время публикации продукта',
        auto_now_add=True,
        help_text='Дата и время публикации продукта',

    )
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        # editable=False,
        verbose_name='Владелец продукта',
    )
    lessons = models.ManyToManyField(
        'Lesson',
        blank=True,
        verbose_name='Уроки',
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Список продуктов'
        ordering = ['name']
        default_related_name = 'products'

    def __str__(self):
        return f'{self.name} by {self.owner}'


class Lesson(models.Model):
    """
    Представляет урок в приложении.

    Поля:
    - name: CharField - Название урока.
    - slug: SlugField - Идентификатор урока, используемый в URL.
    - text: TextField - Описание урока.
    - created_at: DateTimeField - Дата и время публикации урока.
    - video_url: URLField - Ссылка на видео урока.
    - video_duration: IntegerField - Длительность видео урока в секундах.

    Методы:
    - __str__: Возвращает строковое представление объекта урока.
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.',
    )
    text = models.TextField(verbose_name='Описание урока', )
    created_at = models.DateTimeField(
        verbose_name='Дата и время публикации продукта',
        auto_now_add=True,
    )
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        help_text='Ссылка на видео',
        unique=True,
    )
    video_duration = models.IntegerField(
        help_text='Длительность видео в сек.',
        verbose_name='Длительность видео',
    )

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'Список уроков'
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        return (f'Урок {self.name}, '
                f'длительность: {self.video_duration} сек.')


class Access(models.Model):
    """
    Отвечает за доступ, предоставленный пользователю для продукта.

    Поля:
    - user: ForeignKey - Пользователь, которому предоставлен доступ.
    - product: ForeignKey - Продукт, для которого предоставлен доступ.
    - access_granted: BooleanField - Указывает, предоставлен ли доступ или нет.

    Методы:
    - __str__: Возвращает строковое представление объекта доступа.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Продукт',
    )
    access_granted = models.BooleanField(
        default=False,
        verbose_name='Доступ разрешен',
    )

    class Meta:
        verbose_name = 'доступ'
        verbose_name_plural = 'Список доступов'
        ordering = ['-product']
        # Проверяем, что у пользователя нет нескольких
        # доступов к одному продукту.
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product'
            )
        ]

    def __str__(self):
        return f'{self.product}, access granted: {self.access_granted}'


class Statistic(models.Model):
    """
    Представляет статистику просмотра урока пользователем в приложении.

    Поля:
    - user: ForeignKey - Пользователь, который просмотрел урок.
    - product: ForeignKey - Продукт, к которому относится урок.
    - lesson: ForeignKey - Урок, который был просмотрен.
    - time_duration: IntegerField - Количество секунд, просмотренных уроком.
    - last_viewed_date: DateTimeField - Дата и время последнего
      просмотра урока.
    - status: BooleanField - Статус просмотра урока.

    Методы:
    - save: Переопределение метода save() для проверки доступа
     пользователя и связи урока с продуктом.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Продукт',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        verbose_name='Урок',
    )
    time_duration = models.IntegerField(
        verbose_name='Сколько секунд урока просмотрено',
    )
    last_viewed_date = models.DateTimeField(
        verbose_name='Дата и время последнего просмотра',
        blank=True,
        null=True,
    )
    status = models.BooleanField(
        default=False,
        verbose_name='Статус просмотра',
    )

    class Meta:
        verbose_name = 'статистика'
        verbose_name_plural = 'Статистика'
        ordering = ['-product']
        default_related_name = 'statistics'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product', 'lesson'],
                name='unique_user_product_lesson'
            )
        ]

    def save(self, *args, **kwargs):
        """
        Переопределение метода save() для проверки доступа пользователя
        и связи урока с продуктом.

        Если у пользователя есть доступ к продукту и урок связан с продуктом,
        сохраняет объект статистики.
        В противном случае, генерирует исключение ValidationError.
        """
        if (
            self.time_duration // self.lesson.video_duration >=
            settings.PERCENTAGE_STATUS_TRUE
        ):
            self.status = True
        access = Access.objects.filter(
            user=self.user,
            product=self.product,
            access_granted=True
        ).exists()
        if access and self.product.lessons.filter(pk=self.lesson.pk).exists():
            super().save(*args, **kwargs)
        else:
            raise ValidationError(
                "У данного пользователя нет доступа к данному продукту "
                "или урок не связан с продуктом."
            )
