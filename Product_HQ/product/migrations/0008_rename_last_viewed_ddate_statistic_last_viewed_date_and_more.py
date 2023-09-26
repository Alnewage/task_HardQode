# Generated by Django 4.2.5 on 2023-09-26 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_statistic_last_viewed_ddate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistic',
            old_name='last_viewed_dDate',
            new_name='last_viewed_date',
        ),
        migrations.AlterUniqueTogether(
            name='access',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='statistic',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата и время публикации продукта', verbose_name='Дата и время публикации продукта'),
        ),
        migrations.AddConstraint(
            model_name='access',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_user_product'),
        ),
        migrations.AddConstraint(
            model_name='statistic',
            constraint=models.UniqueConstraint(fields=('user', 'product', 'lesson'), name='unique_user_product_lesson'),
        ),
    ]