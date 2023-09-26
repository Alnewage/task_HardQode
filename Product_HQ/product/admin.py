from django.contrib import admin

from product.models import Access, Lesson, Product, Statistic


class LessonInline(admin.TabularInline):
    model = Product.lessons.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели Product.
    """

    inlines = (LessonInline, )

    list_display = (
        'name',
        'slug',
        'text',
        'created_at',
        'owner',
    )

    search_fields = (
        'name',
        'owner',
    )

    list_filter = (
        'owner',
    )

    list_display_links = (
        'name',
        'slug',
    )

    prepopulated_fields = {
        'slug': ('name',),
    }

    filter_horizontal = ('lessons',)


class ProductInline(admin.TabularInline):
    model = Product.lessons.through
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели Lesson.
    """
    inlines = (ProductInline,)

    list_display = (
        'name',
        'slug',
        'text',
        'created_at',
        'video_url',
        'video_duration',
    )

    search_fields = (
        'name',
        'text',
    )

    list_filter = (
        'name',
    )

    list_display_links = (
        'slug',
    )

    save_on_top = True

    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели Access
    (доступ к продуктам для пользователей — студентов).
    """

    list_display = (
        'user',
        'product',
        'access_granted',
    )

    list_editable = (
        'access_granted',
    )

    search_fields = (
        'user',
        'product',
    )

    list_filter = (
        'user',
        'product',
        'access_granted',
    )

    list_display_links = (
        'user',
    )


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели Statistic.
    """

    list_display = (
        'user',
        'product',
        'lesson',
        'time_duration',
        'status',
    )

    readonly_fields = ('status',)

    list_editable = (
        'time_duration',
    )

    search_fields = (
        'user',
        'product',
        'lesson',
    )

    list_filter = (
        'user',
        'product',
        'lesson',
    )

    list_display_links = (
        'user',
        'lesson',
    )


admin.site.empty_value_display = 'Не задано'
admin.site.site_title = 'Администрирование Products_HQ'
admin.site.site_header = 'Администрирование Products_HQ'
