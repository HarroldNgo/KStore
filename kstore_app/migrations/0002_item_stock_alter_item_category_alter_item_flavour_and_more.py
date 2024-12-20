# Generated by Django 5.1.4 on 2024-12-16 19:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kstore_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(blank=True, choices=[('Macarons', 'MACARONS'), ('Cupcakes', 'CUPCAKES'), ('Cakes', 'CAKES'), ('Cookies', 'COOKIES'), ('Brownies', 'BROWNIES'), ('Cake Pops', 'CAKE POPS')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='flavour',
            field=models.CharField(blank=True, choices=[('Vanilla', 'VANILLA'), ('Chocolate', 'CHOCOLATE'), ('Red Velvet', 'RED VELVET'), ('Cookies & Cream', 'COOKIES & CREAM')], max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_code', models.CharField(max_length=11, unique=True)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='kstore_app.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kstore_app.item')),
            ],
        ),
    ]
