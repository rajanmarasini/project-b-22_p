# Generated by Django 3.2.15 on 2022-11-14 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookExchange', '0012_textbooks_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='posts',
            field=models.ManyToManyField(related_name='posted_by', to='BookExchange.Textbooks'),
        ),
    ]