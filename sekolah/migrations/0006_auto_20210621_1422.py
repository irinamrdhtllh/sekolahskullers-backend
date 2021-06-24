# Generated by Django 3.2.4 on 2021-06-21 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0005_auto_20210621_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_finished',
        ),
        migrations.RemoveField(
            model_name='task',
            name='score',
        ),
        migrations.RemoveField(
            model_name='task',
            name='student',
        ),
        migrations.CreateModel(
            name='StudentTaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_finished', models.BooleanField(default=False)),
                ('score', models.IntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekolah.student')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekolah.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='students',
            field=models.ManyToManyField(through='sekolah.StudentTaskStatus', to='sekolah.Student'),
        ),
    ]
