# Generated by Django 5.0.2 on 2024-03-03 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaced_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='atom',
            name='type',
            field=models.TextField(null=True),
        ),
    ]
