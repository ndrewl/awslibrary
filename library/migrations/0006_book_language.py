# Generated by Django 3.0.4 on 2020-04-03 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20200402_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(choices=[('Russian', 'Russian'), ('English', 'English')], max_length=100, null=True),
        ),
    ]
