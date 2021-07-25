# Generated by Django 3.1.5 on 2021-07-21 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furnitureshop', '0008_auto_20210714_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Received', 'Order Received '), ('On The Way', 'On The Way'), ('Order Completed', 'Order Completed'), ('Order Processing', 'Order Processing')], max_length=50),
        ),
    ]
