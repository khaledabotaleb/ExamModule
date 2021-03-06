# Generated by Django 3.0.6 on 2020-05-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers_points', models.IntegerField()),
                ('answer', models.CharField(blank=True, max_length=100, null=True)),
                ('time_to_answer', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_id', models.IntegerField()),
                ('quiz_headline', models.CharField(blank=True, max_length=100, null=True)),
                ('quiz_creation_time', models.DateTimeField(auto_now_add=True)),
                ('quiz_real_time', models.IntegerField()),
                ('quiz_setion_time', models.IntegerField()),
                ('quiz_is_launched', models.BooleanField(default=False)),
            ],
        ),
    ]
