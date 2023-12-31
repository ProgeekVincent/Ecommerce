# Generated by Django 4.2.4 on 2023-09-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/products/others/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('slug', models.SlugField(max_length=300, unique=True)),
                ('image', models.ImageField(upload_to='images/products/main/', verbose_name='main image')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('available', models.BooleanField(default=True)),
                ('other_image', models.ManyToManyField(to='store.image', verbose_name='other images')),
            ],
        ),
    ]
