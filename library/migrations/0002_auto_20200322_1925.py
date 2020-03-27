# Generated by Django 3.0.4 on 2020-03-22 19:25

from django.db import migrations, models
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='year',
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=library.models._get_updload_file_path),
        ),
        migrations.AlterField(
            model_name='book',
            name='goodreads_link',
            field=models.URLField(blank=True),
        ),
    ]