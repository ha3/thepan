# Generated by Django 2.2 on 2019-05-31 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findmeal', '0015_recipe_prep_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='prep_time',
            field=models.DurationField(),
        ),
    ]