# Generated by Django 3.1.2 on 2020-12-12 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommrecipe',
            name='all_recipe_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]