# Generated by Django 5.1.3 on 2024-12-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapp', '0013_remove_submission_file_submission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='courses',
            field=models.ManyToManyField(null=True, related_name='teachers', to='lapp.course'),
        ),
    ]
