# Generated by Django 4.2.5 on 2023-10-20 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_users_is_first_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='is_first_admin',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='users',
            name='is_pending_approval',
            field=models.BooleanField(),
        ),
    ]
