# Generated by Django 3.0.5 on 2020-04-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0014_auto_20200416_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
    ]