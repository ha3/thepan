# Generated by Django 2.2 on 2019-05-31 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findmeal', '0009_recipe_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='rateuser',
            new_name='rate_count',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='prep',
        ),
    ]