# Generated by Django 3.1.1 on 2021-03-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culinary_post', '0002_auto_20210319_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
