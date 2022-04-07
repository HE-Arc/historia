# Generated by Django 3.2.11 on 2022-04-07 18:57

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
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('historicPeriod', models.CharField(default='Unknown', max_length=400)),
                ('domain', models.CharField(default='Unknown', max_length=200)),
                ('category', models.CharField(default='Unknown', max_length=400)),
                ('birth', models.CharField(default='Unknown', max_length=100)),
                ('land', models.CharField(default='Unknown', max_length=200)),
                ('text', models.CharField(max_length=4000)),
                ('image', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField(max_length=2000)),
                ('opt_one', models.CharField(max_length=200)),
                ('opt_two', models.CharField(max_length=200)),
                ('opt_three', models.CharField(max_length=200)),
                ('opt_four', models.CharField(max_length=200)),
                ('answer', models.IntegerField(default=1)),
                ('is_correct', models.BooleanField(default=False)),
                ('character', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historiaapp.card')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField(max_length=2000)),
                ('score_quiz', models.IntegerField(default=0)),
                ('questions', models.ManyToManyField(related_name='questions', to='historiaapp.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('date', models.DateField(db_index=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='historiaapp.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
