# Generated by Django 4.2.4 on 2023-08-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="invitation_code",
            field=models.CharField(
                blank=True,
                default="nNtpmT",
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
