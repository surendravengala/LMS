# Generated by Django 5.1.3 on 2024-11-25 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapp', '0004_alter_student_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mail',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(max_length=50),
        ),
    ]