# Generated by Django 5.1.1 on 2025-02-25 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application_1', '0003_alter_projet_user_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('file_id', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application_1.projet_user')),
            ],
        ),
    ]
