# Generated by Django 4.2.3 on 2024-05-18 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finapp', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintitle', models.CharField(max_length=200)),
                ('maintitle2', models.CharField(max_length=200)),
                ('card1', models.CharField(max_length=200)),
                ('description1', models.CharField(max_length=200)),
                ('card2', models.CharField(max_length=200)),
                ('description2', models.CharField(max_length=200)),
                ('card3', models.CharField(max_length=200)),
                ('description3', models.CharField(max_length=200)),
                ('card4', models.CharField(max_length=200)),
                ('description4', models.CharField(max_length=200)),
            ],
        ),
    ]
