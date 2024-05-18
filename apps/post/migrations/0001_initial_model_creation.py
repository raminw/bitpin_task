# Generated by Django 4.2.13 on 2024-05-18 14:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField()),
                ('text', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('rate_count', models.PositiveIntegerField(default=0)),
                ('total_rate', models.PositiveIntegerField(default=0)),
                ('average_rate', models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('last_rate_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'post',
                'ordering': ['id'],
            },
        ),
    ]