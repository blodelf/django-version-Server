# Generated by Django 4.0.4 on 2022-05-29 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_users_all_title_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users_all',
            name='admin_level',
            field=models.IntegerField(blank=True, default='1', verbose_name='admin_level'),
        ),
    ]
