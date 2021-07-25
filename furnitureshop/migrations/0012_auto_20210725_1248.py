# Generated by Django 3.1.5 on 2021-07-25 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furnitureshop', '0011_auto_20210724_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=20)),
                ('phone', models.CharField(max_length=30)),
                ('messae', models.TextField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Completed', 'Order Completed'), ('Order Processing', 'Order Processing'), ('On The Way', 'On The Way'), ('Order Received', 'Order Received ')], max_length=50),
        ),
    ]