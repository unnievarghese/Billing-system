# Generated by Django 3.1.6 on 2021-03-13 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.CharField(max_length=12, unique=True)),
                ('bill_date', models.DateField(auto_now=True)),
                ('customer_name', models.CharField(max_length=60)),
                ('phone_number', models.CharField(max_length=12)),
                ('bill_total', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('purchase_date', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.product')),
            ],
        ),
        migrations.CreateModel(
            name='ordelines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_qty', models.FloatField()),
                ('amount', models.FloatField()),
                ('bill_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.order')),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.product')),
            ],
        ),
    ]
