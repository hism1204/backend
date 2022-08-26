# Generated by Django 4.0.5 on 2022-08-26 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_merge_20220825_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=200, null=True)),
                ('upload_user_id', models.CharField(max_length=45, null=True)),
                ('upload_target_building_name', models.IntegerField(null=True)),
                ('key', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200, null=True)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='home.account')),
            ],
        ),
        migrations.CreateModel(
            name='Voice_to_Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voice_to_text', models.CharField(max_length=200, null=True)),
                ('upload_user_id', models.CharField(max_length=45, null=True)),
                ('upload_target_building_name', models.IntegerField(null=True)),
                ('key', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='floor',
            name='drawing_id',
        ),
        migrations.AddField(
            model_name='floor',
            name='drawing',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='raw_data',
            name='picture',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Drawing',
        ),
    ]
