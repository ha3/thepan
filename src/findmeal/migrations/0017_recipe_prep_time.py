# Generated by Django 2.2.1 on 2019-07-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findmeal', '0016_remove_recipe_prep_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='prep_time',
            field=models.DurationField(),
            preserve_default=False,
        ),
    ]