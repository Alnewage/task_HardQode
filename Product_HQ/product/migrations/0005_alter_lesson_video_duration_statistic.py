# Generated by Django 4.2.5 on 2023-09-25 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0004_alter_product_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_duration',
            field=models.IntegerField(help_text='Длительность видео в сек.', verbose_name='Длительность видео'),
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_duration', models.IntegerField(verbose_name='Сколько секунд урока просмотрено')),
                ('status', models.BooleanField(default=False, verbose_name='Статус просмотренного урока')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.lesson', verbose_name='Урок')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'статистика',
                'verbose_name_plural': 'Статистика',
                'ordering': ['-product'],
                'default_related_name': 'statistics',
            },
        ),
    ]
