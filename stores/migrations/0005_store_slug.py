# Generated by Django 3.0.5 on 2020-04-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_auto_20200415_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]