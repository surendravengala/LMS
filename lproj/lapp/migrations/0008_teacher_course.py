# Generated by Django 5.1.3 on 2024-11-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapp', '0007_coursevideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='course',
            field=models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('CoreJava', 'Core Java')], default='python', max_length=50),
            preserve_default=False,
        ),
    ]
