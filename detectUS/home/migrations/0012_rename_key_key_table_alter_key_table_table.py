# Generated by Django 4.0.5 on 2022-08-26 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_key_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Key',
            new_name='Key_Table',
        ),
        migrations.AlterModelTable(
            name='key_table',
            table='key_table',
        ),
    ]
