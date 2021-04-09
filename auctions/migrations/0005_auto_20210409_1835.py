# Generated by Django 3.1.3 on 2021-04-09 18:35

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210406_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('CF', 'Clothing/Fashion'), ('BOOKS', 'Books'), ('MMG', 'Movies, Music, & Games'), ('ELEC', 'Electronics'), ('COMP', 'Computers'), ('SMART', 'Smart Home'), ('HGT', 'Home, Garden, & Tools'), ('PET', 'Pet Supplies'), ('FG', 'Food & Grocery'), ('BH', 'Beauty & Health'), ('TKB', 'Toys, Kids, & Baby'), ('HAND', 'Handmade'), ('SPORTS', 'Sports'), ('OUT', 'Outdoors'), ('AUTOIND', 'Automotive & Industrial'), ('OTHER', 'Other')], default='CF', max_length=100),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('winner', models.BooleanField(default=False)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mybid', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
            ],
        ),
    ]
