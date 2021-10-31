# Generated by Django 3.1.5 on 2021-07-26 03:07

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import furnitureshop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with the username already exits.'}, help_text='Required. 150 characters or fewer.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(default='test@gmail.com', max_length=254, unique=True, verbose_name='email address')),
                ('full_name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether user can log into admin or not.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates wheter this should be treated as activeUnselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date_joined')),
                ('email_varified', models.BooleanField(default=False, help_text='Designates whether users email is varified.', verbose_name='email_varified')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', furnitureshop.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amout', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('phone', models.CharField(max_length=30)),
                ('message', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='pics')),
                ('marked_price', models.PositiveIntegerField()),
                ('selling_price', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('discount', models.BooleanField(default=False)),
                ('return_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('catagory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='furnitureshop.catagory')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_by', models.CharField(max_length=200)),
                ('shipping_address', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subtotal', models.PositiveIntegerField(default=0)),
                ('discount', models.PositiveIntegerField(default=0)),
                ('total', models.PositiveIntegerField(default=0)),
                ('order_status', models.CharField(choices=[('Order Received', 'Order Received '), ('On The Way', 'On The Way'), ('Order Completed', 'Order Completed'), ('Order Processing', 'Order Processing')], max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='furnitureshop.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Cartproduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('quantaty', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField(default=0)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='furnitureshop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='furnitureshop.product')),
            ],
        ),
    ]
