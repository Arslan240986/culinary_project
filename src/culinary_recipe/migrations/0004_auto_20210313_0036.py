# Generated by Django 3.1.1 on 2021-03-13 00:36

import culinary_recipe.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culinary_recipe', '0003_auto_20210311_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='poster',
            field=models.ImageField(upload_to=culinary_recipe.models.get_poster_image_filepath, verbose_name='Постер'),
        ),
        migrations.AlterField(
            model_name='step',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=culinary_recipe.models.get_steps_image_filepath, verbose_name='Фото'),
        ),
    ]