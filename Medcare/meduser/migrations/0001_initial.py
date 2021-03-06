# Generated by Django 3.0.8 on 2020-08-15 19:52

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import meduser.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('user_cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('symbol', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('Description', models.TextField(blank=True, null=True)),
                ('product_name', models.CharField(max_length=30, null=True)),
                ('mobile', models.DecimalField(decimal_places=0, max_digits=10)),
                ('email', models.EmailField(max_length=255)),
                ('address', models.TextField()),
                ('product_category_text', models.CharField(blank=True, max_length=30, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(blank=True, null=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('donated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Donations',
            },
        ),
        migrations.CreateModel(
            name='ProductsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Products categories',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('thumb_image', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/product_images/products/', location='D:\\Studies\\Final year project\\Medcare\\product_images/products/'), upload_to=meduser.models.get_image_filenames, verbose_name='Image')),
                ('Description', models.TextField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('available', models.BooleanField()),
                ('active', models.BooleanField()),
                ('expected_return_date', models.DateField(blank=True, null=True)),
                ('deposite_Amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('length', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('width', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('current_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_user', to=settings.AUTH_USER_MODEL)),
                ('donated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donated_user', to=settings.AUTH_USER_MODEL)),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduser.ProductsCategory')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/product_images/products/', location='D:\\Studies\\Final year project\\Medcare\\product_images/products/'), upload_to=meduser.models.get_image_filename, verbose_name='Image')),
                ('donation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduser.Donations')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduser.Products')),
            ],
            options={
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.AddField(
            model_name='donations',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduser.Products'),
        ),
        migrations.AddField(
            model_name='donations',
            name='product_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduser.ProductsCategory'),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduser.Currency')),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_date', models.DateField(blank=True, null=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('line_total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='meduser.Cart')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduser.Products')),
            ],
            options={
                'verbose_name_plural': 'Cart Items',
            },
        ),
    ]
