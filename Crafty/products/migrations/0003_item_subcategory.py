# Generated by Django 4.2.16 on 2024-12-01 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_item_subcategory_item_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='products.subcategory'),
        ),
    ]