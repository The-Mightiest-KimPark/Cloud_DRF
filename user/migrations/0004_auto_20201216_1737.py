# Generated by Django 3.1.4 on 2020-12-16 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_merge_20201216_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]