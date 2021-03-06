# Generated by Django 3.0.6 on 2020-05-12 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Question', '0001_initial'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Teacher'),
        ),
        migrations.AddField(
            model_name='rate',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='Question.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Teacher'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Subject'),
        ),
        migrations.AddField(
            model_name='mcq',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mcq', to='Question.Question'),
        ),
    ]
