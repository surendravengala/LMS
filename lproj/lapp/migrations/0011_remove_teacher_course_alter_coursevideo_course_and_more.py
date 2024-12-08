# Generated by Django 5.1.3 on 2024-11-30 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapp', '0010_alter_coursevideo_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='course',
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='course',
            field=models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('CoreJava', 'Core Java')], max_length=50),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('CoreJava', 'Core Java')], max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('students', models.ManyToManyField(related_name='assignments', to='lapp.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lapp.teacher')),
            ],
        ),
    ]