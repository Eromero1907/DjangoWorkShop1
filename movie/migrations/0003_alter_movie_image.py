# Generated by Django 5.1.6 on 2025-03-03 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_movie_genre_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(default='movie/images/default.png', upload_to='movie/images/'),
        ),
    ]
