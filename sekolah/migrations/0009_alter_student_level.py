# Generated by Django 3.2.4 on 2021-06-24 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0008_rename_is_finished_studenttaskstatus_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')], default=1, max_length=3),
        ),
    ]