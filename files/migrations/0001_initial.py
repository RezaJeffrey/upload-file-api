# Generated by Django 4.1.4 on 2023-01-01 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import files.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_time', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('file', models.FileField(upload_to=files.models.user_directory_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
