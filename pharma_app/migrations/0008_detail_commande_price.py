# Generated by Django 4.1.3 on 2024-11-22 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharma_app", "0007_commande_nbr_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="detail_commande",
            name="price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]