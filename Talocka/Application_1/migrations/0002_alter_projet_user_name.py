# Generated by Django 5.1.1 on 2025-02-18 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application_1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet_user',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
