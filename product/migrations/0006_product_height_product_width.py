# Generated by Django 4.2.7 on 2023-12-03 13:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0005_alter_category_options_alter_images_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="height",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="width",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
