# Generated by Django 3.2.8 on 2021-12-12 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notesApp', '0002_auto_20211212_0051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='commenter',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='user',
            new_name='author',
        ),
    ]