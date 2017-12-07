# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-07 03:12
from __future__ import unicode_literals

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
            name='Admin',
            fields=[
                ('Admin_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Admin_Email', models.CharField(max_length=32)),
                ('Name', models.CharField(max_length=32)),
                ('Password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=32)),
                ('Year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Location', models.CharField(max_length=32)),
                ('Most_Popular_Album_Name', models.IntegerField()),
                ('Most_Popular_Song_ID', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Basic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DOB', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RateAlbums',
            fields=[
                ('Rate_Album_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Stars', models.IntegerField()),
                ('Rate_Date', models.DateField()),
                ('Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Album')),
                ('Owner_User_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='RateSongs',
            fields=[
                ('Rate_Song_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Stars', models.IntegerField()),
                ('Rate_Date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('Review_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Deleted', models.IntegerField()),
                ('Reviewed', models.IntegerField()),
                ('Flagged_Date', models.DateField()),
                ('Review_Date', models.DateField()),
                ('Admin_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Admin')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('Song_ID', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=32)),
                ('Plays', models.IntegerField()),
                ('Album_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Users'),
        ),
        migrations.AddField(
            model_name='review',
            name='Song_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Song'),
        ),
        migrations.AddField(
            model_name='ratesongs',
            name='Rater_User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Users'),
        ),
        migrations.AddField(
            model_name='ratesongs',
            name='Song_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Song'),
        ),
        migrations.AddField(
            model_name='ratealbums',
            name='Rater_User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Users'),
        ),
        migrations.AddField(
            model_name='basic',
            name='User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Users'),
        ),
        migrations.AddField(
            model_name='artist',
            name='User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Users'),
        ),
        migrations.AddField(
            model_name='album',
            name='User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harryslist.Users'),
        ),
    ]
