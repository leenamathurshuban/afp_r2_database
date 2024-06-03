# Generated by Django 5.0.6 on 2024-06-01 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_delete_warehouse_alter_role_role_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='role_image/'),
        ),
        migrations.AddField(
            model_name='role',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_name',
            field=models.CharField(blank=True, default='Active', max_length=100, null=True, unique=True),
        ),
    ]
