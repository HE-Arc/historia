# Generated by Django 3.2.11 on 2022-03-15 20:41

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
                ('text', models.CharField(max_length=2000)),
                ('opt_one', models.CharField(max_length=200)),
                ('opt_two', models.CharField(max_length=200)),
                ('opt_three', models.CharField(max_length=200)),
                ('opt_four', models.CharField(max_length=200)),
                ('ans_one', models.BooleanField(default=False)),
                ('ans_two', models.BooleanField(default=False)),
                ('ans_three', models.BooleanField(default=False)),
                ('ans_four', models.BooleanField(default=False)),
                ('character', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historiaapp.card')),
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
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudo', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
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
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historiaapp.user')),
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
