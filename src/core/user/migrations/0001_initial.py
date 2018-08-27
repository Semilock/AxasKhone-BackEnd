# Generated by Django 2.1 on 2018-08-27 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_username', models.CharField(blank=True, max_length=200)),
                ('fullname', models.CharField(blank=True, max_length=200)),
                ('bio', models.CharField(blank=True, max_length=400)),
                ('profile_pic', models.ImageField(blank=True, max_length=500, upload_to='')),
                ('followers_number', models.IntegerField(blank=True, default=0)),
                ('following_number', models.IntegerField(blank=True, default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]