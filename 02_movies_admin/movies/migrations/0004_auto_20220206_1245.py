# Generated by Django 3.2 on 2022-02-06 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20220206_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genrefilmwork',
            old_name='film_work_id',
            new_name='film_work',
        ),
        migrations.RenameField(
            model_name='genrefilmwork',
            old_name='genre_id',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='personfilmwork',
            old_name='film_work_id',
            new_name='film_work',
        ),
        migrations.RenameField(
            model_name='personfilmwork',
            old_name='person_id',
            new_name='person',
        ),
    ]