# Generated by Django 2.2 on 2019-05-31 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findmeal', '0010_auto_20190531_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='prep_times',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
