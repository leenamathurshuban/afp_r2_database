# Generated by Django 4.2 on 2024-06-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_bar_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bar_code',
            field=models.FileField(blank=True, default='bar_code/default_user.jpeg', null=True, upload_to='bar_code/'),
        ),
    ]
