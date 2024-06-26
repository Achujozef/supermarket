# Generated by Django 4.2.7 on 2024-05-05 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="shop",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="app.shop"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="shop",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="app.shop"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="shop",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="app.shop"
            ),
        ),
    ]
