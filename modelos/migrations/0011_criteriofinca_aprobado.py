# Generated by Django 3.2.8 on 2021-12-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0010_auto_20211206_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='criteriofinca',
            name='aprobado',
            field=models.BooleanField(default=False),
        ),
    ]
