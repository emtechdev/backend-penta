# Generated by Django 5.0.7 on 2024-07-21 12:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_supervisor_assign_supervisor_approved_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assign',
            unique_together={('task', 'user')},
        ),
    ]
