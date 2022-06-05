# Generated by Django 4.0.4 on 2022-05-28 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_delete_users_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='users_history',
            fields=[
                ('id', models.IntegerField(db_column='user_id', default=0, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('action', models.CharField(blank=True, choices=[('CREATION', 'CREATION'), ('WARNING', 'WARNING'), ('CLOSING', 'CLOSING'), ('ACTIVATION', 'ACTIVATION'), ('CHPASS', 'CHPASS'), ('EXT_EXPIRE', 'EXT_EXPIRE'), ('CHDATA', 'CHDATA')], default='CREATION', max_length=20, verbose_name='Action')),
                ('creator', models.CharField(blank=True, max_length=16, verbose_name='creator')),
                ('reason', models.TextField(blank=True, verbose_name='reason')),
                ('ip', models.TextField(blank=True, max_length=15, verbose_name='ip')),
            ],
            options={
                'verbose_name': 'users history',
                'verbose_name_plural': 'users history',
            },
        ),
    ]