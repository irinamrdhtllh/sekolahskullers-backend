# Generated by Django 3.2.4 on 2021-06-29 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0015_auto_20210629_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='student',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sekolah.student'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='class_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missions', to='sekolah.classyear'),
        ),
    ]