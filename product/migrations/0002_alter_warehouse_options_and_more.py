# Generated by Django 5.0.6 on 2024-06-01 05:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='warehouse',
            options={'verbose_name_plural': 'WareHouse'},
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='warehouse_uid',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]