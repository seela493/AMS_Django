# Generated by Django 5.1.3 on 2024-12-05 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]