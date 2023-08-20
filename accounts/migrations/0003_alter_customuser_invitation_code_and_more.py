# Generated by Django 4.2.4 on 2023-08-20 23:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_customuser_invitation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="invitation_code",
            field=models.CharField(
                blank=True,
                default="vNNn8y",
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="invited_by",
            field=models.ForeignKey(
                blank=True,
                max_length=6,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=16,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                        regex="^\\+\\d{8,15}$",
                    )
                ],
            ),
        ),
    ]
