# Generated by Django 4.2 on 2024-06-06 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_bar_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bar_code',
            field=models.FileField(blank=True, null=True, upload_to='bar_code/'),
        ),
    ]
