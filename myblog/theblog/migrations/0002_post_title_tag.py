# Generated by Django 3.0.6 on 2020-05-25 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title_tag',
            field=models.CharField(default='Blog Post', max_length=255),
        ),
    ]
