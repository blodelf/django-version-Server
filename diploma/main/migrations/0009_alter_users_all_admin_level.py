# Generated by Django 4.0.4 on 2022-05-27 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_users_all_contr_answ_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users_all',
            name='admin_level',
            field=models.IntegerField(blank=True, default='0', verbose_name='admin_level'),
        ),
    ]
