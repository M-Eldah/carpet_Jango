# Generated by Django 4.2.7 on 2023-12-06 17:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0013_alter_category_options"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Category",
            new_name="ProductCategory",
        ),
    ]
