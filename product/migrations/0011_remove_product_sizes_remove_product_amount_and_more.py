# Generated by Django 4.2.7 on 2023-12-06 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0010_remove_product_height_remove_product_width_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="Sizes",
        ),
        migrations.RemoveField(
            model_name="product",
            name="amount",
        ),
        migrations.AlterField(
            model_name="productimg",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="productimgs",
                to="product.product",
            ),
        ),
        migrations.CreateModel(
            name="ProductSizes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Sizes", models.CharField(default="Storage", max_length=255)),
                ("amount", models.IntegerField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="productsizes",
                        to="product.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Size",
                "verbose_name_plural": "Sizes",
                "ordering": ("-product",),
            },
        ),
    ]
