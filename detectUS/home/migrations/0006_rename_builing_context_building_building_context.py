# Generated by Django 4.0.6 on 2022-07-28 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_floor_building_id_issue_building_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='builing_context',
            new_name='building_context',
        ),
    ]
