# Generated by Django 4.1.2 on 2022-11-26 06:47

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order',
            field=django_mysql.models.ListCharField(models.CharField(max_length=4), max_length=25, size=5),
        ),
    ]
