# Generated by Django 4.1.3 on 2024-11-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharma_app", "0005_commande_panier_commande_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="commande",
            name="sub_total",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="commande",
            name="tva",
            field=models.FloatField(blank=True, null=True),
        ),
    ]