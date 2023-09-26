# Generated by Django 4.2.5 on 2023-09-25 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0005_alter_lesson_video_duration_statistic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Название'),
        ),
        migrations.AlterUniqueTogether(
            name='access',
            unique_together={('user', 'product')},
        ),
    ]
