# Generated by Django 4.0.4 on 2022-05-02 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_requests_id_req'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='id_req',
            field=models.PositiveIntegerField(verbose_name='ID'),
        ),
    ]
