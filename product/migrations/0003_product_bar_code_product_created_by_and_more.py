# Generated by Django 4.2 on 2024-06-06 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_product_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bar_code',
            field=models.FileField(blank=True, null=True, upload_to='bar_code/'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='warehouse_name',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
