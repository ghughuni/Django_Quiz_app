# Generated by Django 4.1.7 on 2023-05-08 14:38

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ChooseAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField(default=False, verbose_name='Is this the question correct?')),
                ('text', models.TextField(verbose_name='Text of responses')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text of Question')),
                ('max_score', models.DecimalField(decimal_places=2, default=3, max_digits=6, verbose_name='Max score')),
                ('category', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='quiz.category')),
            ],
        ),
        migrations.CreateModel(
            name='QuizUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='total_score')),
                ('choose_category', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='choose_category')),
                ('users', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsAnswered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField()),
                ('correct', models.BooleanField(default=False, verbose_name='Is this the correct answer?')),
                ('obtained_score', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Obtained Score')),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.chooseanswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('quizUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='quiz.quizusers')),
            ],
        ),
        migrations.AddField(
            model_name='chooseanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='quiz.question'),
        ),
    ]
