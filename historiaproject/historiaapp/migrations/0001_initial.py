# Generated by Django 3.2.11 on 2022-03-21 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(default='', upload_to='images/')),
                ('birth', models.CharField(max_length=20)),
                ('text', models.CharField(max_length=4000)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('question', models.CharField(max_length=200)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historiaapp.card')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.TimeField(auto_now_add=True)),
                ('end_time', models.TimeField(auto_now_add=True)),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historiaapp.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionByQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.ManyToManyField(to='historiaapp.Question')),
                ('quiz_id', models.ManyToManyField(to='historiaapp.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerText', models.CharField(max_length=200)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historiaapp.question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_option_id', models.ManyToManyField(to='historiaapp.AnswerOptions')),
                ('score_id', models.ManyToManyField(to='historiaapp.Score')),
            ],
        ),
    ]
